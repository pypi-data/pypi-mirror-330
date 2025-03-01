"""
GENERAL
=======
Double emulsion project code library.
"""
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from skimage import io, draw, filters
from myimagelib.myImageLib import readdata
from myimagelib.pivLib import read_piv, PIV, PIV_masked
from scipy.ndimage import gaussian_filter1d
from myimagelib.fit_circle_utils import fit_circle
import myimagelib.corrTrack
import os
import trackpy as tp

class droplet_image:
    """Container of functions related to confocal droplet images"""
    def __init__(self, image_sequence, fps, mpp):
        """image_sequence: dataframe of image dir info, readdata return value
        mask: image mask, the same as PIV mask
        xy0: 2-tuple of droplet initial coordinates, read from positions.csv file
        mask_shape: shape of the circular mask, 2-tuple specifying the rect bounding box of the mask, typically a square
                    read from positions.csv file"""
        self.sequence = image_sequence
        self.fps = fps
        self.mpp = mpp
    def __repr__(self):
        I0 = io.imread(self.sequence.iloc[0, 1])
        return "length: {0:d}, image size: {1}, fps: {2:.1f}, mpp: {3:.2f}".format(
                len(self.sequence), str(I0.shape), self.fps, self.mpp)
    def __len__(self):
        return len(self.sequence)
    def process_first_image(self, mask):
        """Compare the provided mask (template) with the first image.
        If the maximum correlation is at the center of the image, the input mask should be correct.
        This function also records the measured center coordinates (xc, yc), for computing the offset."""
        img = io.imread(self.sequence.Dir[0])
        h, w = img.shape
        xy, pkv = corrTrack.track_spheres(img, mask, 1, subpixel=True)
        xyc = np.flip(xy.squeeze())
        # The center coords should be very close to the image center (w/2, h/2)
        diff = np.square(xyc-np.array([w/2, h/2])).sum()
        if diff > 10: # this threshold is arbitrary
            print("The detected center is {:.1f} pixels from the image center, check if the input mask is correct.".format(diff**0.5))
        return xyc
    def droplet_traj(self, mask, xy0):
        xyc = self.process_first_image(mask)
        xym_list = []
        for num, i in self.sequence.iterrows():
            print("Tracking droplet: {}".format(self.get_image_name(num)), end="\r")
            img = io.imread(i.Dir)
            xy, pkv = corrTrack.track_spheres(img, mask, 1)
            xym_list.append(np.flip(xy.squeeze()))
        xym = np.stack(xym_list, axis=0)
        traj = self.sequence.copy()
        traj = traj.assign(x=xy0[0] + xym[:, 0] - xyc[0], y=xy0[1] + xym[:, 1] - xyc[1])
        self.traj = traj
        return traj
    def get_cropped_image(self, index, traj, mask_shape):
        """Retrieve cropped image by index.
        Mar 10, 2022 -- boundary protection."""
        x = int(traj.x[index])
        y = int(traj.y[index])
        h, w = mask_shape
        x0 = x - w // 2
        x1 = x0 + w
        y0 = y - h // 2
        y1 = y0 + h
        img = self.get_image(index)
        ih, iw = img.shape
        cropped = img[max(y0, 0): min(y1, ih), max(x0, 0): min(x1, iw)]
        return cropped
    def get_image(self, index):
        """Retrieve image by index"""
        imgDir = self.sequence.Dir[index]
        img = io.imread(imgDir)
        return img
    def check_traj(self, traj, mask_shape, n=10):
        """Check the droplet finding.
        traj: DataFrame containing columns 'x' and 'y'
        mask_shape: 2-tuple, (width, height)
        n: total number of frames to inspect, default to 10"""
        interval = len(traj) // n
        count = 0
        for num, i in traj[::interval].iterrows():
            fig, ax = plt.subplots()
            img = io.imread(i.Dir)
            elli = Ellipse((i.x, i.y), *mask_shape, facecolor=(0,0,0,0), lw=1, edgecolor="red")
            ax.imshow(img, cmap="gray")
            ax.add_patch(elli)
            count += 1
            if count >= n:
                break
    def get_image_name(self, index):
        return self.sequence.Name[index]
    def fixed_mask_piv(self, winsize, overlap, mask_dir):
        """Edit:
        08092022 -- Return PIV results instead of saving to file.
                    Remove arg save_folder .
                    Remove arg dt, add required arg fps in __init__ instead
        """
        dt = 1 / self.fps
        mask = io.imread(mask_dir)
        data = {}
        for i0, i1 in zip(self.sequence.index[::2], self.sequence.index[1::2]):
            I0 = self.get_image(i0)
            I1 = self.get_image(i1)
            x, y, u, v = PIV_masked(I0, I1, winsize, overlap, dt, mask)
            # generate dataframe and save to file
            tmp = pd.DataFrame({"x": x.flatten(), "y": y.flatten(), "u": u.flatten(), "v": v.flatten()})
            data["{0}-{1}".format(self.get_image_name(i0), self.get_image_name(i1))] = tmp
            # data.to_csv(os.path.join(save_folder, "{0}-{1}.csv".format(self.get_image_name(i0), self.get_image_name(i1))), index=False)
        params = {"winsize": winsize,
                  "overlap": overlap,
                  "dt": dt,
                  "mask_dir": mask_dir}
        # with open(os.path.join(save_folder, "piv_params.json"), "w") as f:
        #     json.dump(params, f)
        return data, params
    def piv_overlay_fixed(self, piv_folder, out_folder, sparcity=1):
        """Draw PIV overlay for fixed mask PIV data (unify old code in class)"""
        def determine_arrow_scale(u, v, sparcity):
            row, col = u.shape
            return max(np.nanmax(u), np.nanmax(v)) * col / sparcity / 1.5
        if os.path.exists(out_folder) == False:
            os.makedirs(out_folder)
        l = readdata(piv_folder, "csv")
        # determine scale using the first frame
        x, y, u, v = read_piv(l.Dir[0])
        scale = determine_arrow_scale(u, v, sparcity)

        for num, i in l.iterrows():
            name = i.Name.split("-")[0]
            index = self.sequence.loc[self.sequence.Name==name].index[0]
            img = self.get_image(index)
            x, y, u, v = read_piv(i.Dir)
            # sparcify
            row, col = x.shape
            xs = x[0:row:sparcity, 0:col:sparcity]
            ys = y[0:row:sparcity, 0:col:sparcity]
            us = u[0:row:sparcity, 0:col:sparcity]
            vs = v[0:row:sparcity, 0:col:sparcity]
            # plot quiver
            dpi = 300
            figscale = 1
            w, h = img.shape[1] / dpi, img.shape[0] / dpi
            fig = Figure(figsize=(w*figscale, h*figscale)) # on some server `plt` is not supported
            canvas = FigureCanvas(fig) # necessary?
            ax = fig.add_axes([0, 0, 1, 1])
            ax.imshow(img, cmap='gray')
            ax.quiver(xs, ys, us, vs, color='yellow', width=0.003, \
                        scale=scale, scale_units='width') # it's better to set a fixed scale, see *Analysis of Collective Motions in Droplets* Section IV.A.2 for more info.
            ax.axis('off')
            # save figure
            fig.savefig(os.path.join(out_folder, name + '.jpg'), dpi=dpi)
    def moving_mask_piv(self, save_folder, winsize, overlap, dt, mask_dir, xy0, mask_shape):
        """Perform moving mask PIV and save PIV results and parameters in save_folder"""
        # create save_folder
        if os.path.exists(save_folder) == False:
            os.makedirs(save_folder)
        # save params in .json file, so that only PIV data are saved in .csv files
        params = {"winsize": winsize,
                  "overlap": overlap,
                  "dt": dt,
                  "mask_dir": mask_dir,
                  "droplet_initial_position (xy0)": (int(xy0[0]), int(xy0[1])),
                  "mask_shape": (int(mask_shape[0]), int(mask_shape[1]))}
        # save traj data in .json file, so that only PIV data are saved in .csv files
        with open(os.path.join(save_folder, "piv_params.json"), "w") as f:
            json.dump(params, f)
        # track droplet
        mask = io.imread(mask_dir)
        traj = self.droplet_traj(mask, xy0)
        traj.to_json(os.path.join(save_folder, "droplet_traj.json"))
        # PIV
        print("")
        n = 0
        for i0, i1 in zip(self.sequence.index[::2], self.sequence.index[1::2]):
            name0 = self.get_image_name(i0)
            name1 = self.get_image_name(i1)
            print("PIV: {0}-{1}".format(name0, name1), end="\r")
            I0 = self.get_cropped_image(i0, traj, mask_shape)
            I1 = self.get_cropped_image(i1, traj, mask_shape)
            x, y, u, v = PIV(I0, I1, winsize, overlap, dt)
            # apply (circular) mask to u and v: implement in the piv_data class

            # generate dataframe and save to file
            data = pd.DataFrame({"x": x.flatten(), "y": y.flatten(), "u": u.flatten(), "v": v.flatten()})
            data.to_csv(os.path.join(save_folder, "{0}-{1}.csv".format(self.get_image_name(i0), self.get_image_name(i1))), index=False)
            n += 1
            if n != 0 and n % 100 == 0:
                print("PIV: {0}-{1}".format(name0, name1))
    def piv_overlay_moving(self, piv_folder, out_folder, traj, piv_params, sparcity=1, crop=True):
        """Draw PIV overlay for moving mask piv data (only on cropped images)"""
        def determine_arrow_scale(u, v, sparcity):
            row, col = u.shape
            return max(np.nanmax(u), np.nanmax(v)) * col / sparcity / 1.5
        if os.path.exists(out_folder) == False:
            os.makedirs(out_folder)
        mask_shape = piv_params["mask_shape"]
        l = readdata(piv_folder, "csv")
        # determine scale using the first frame
        x, y, u, v = read_piv(l.Dir[0])
        scale = determine_arrow_scale(u, v, sparcity)

        for num, i in l.iterrows():
            name = i.Name.split("-")[0]
            index = self.sequence.loc[self.sequence.Name==name].index[0]
            img = self.get_cropped_image(index, traj, mask_shape)
            x, y, u, v = read_piv(i.Dir)
            # sparcify
            row, col = x.shape
            xs = x[0:row:sparcity, 0:col:sparcity]
            ys = y[0:row:sparcity, 0:col:sparcity]
            us = u[0:row:sparcity, 0:col:sparcity]
            vs = v[0:row:sparcity, 0:col:sparcity]
            # plot quiver
            dpi = 300
            figscale = 1
            w, h = img.shape[1] / dpi, img.shape[0] / dpi
            fig = Figure(figsize=(w*figscale, h*figscale)) # on some server `plt` is not supported
            canvas = FigureCanvas(fig) # necessary?
            ax = fig.add_axes([0, 0, 1, 1])
            ax.imshow(img, cmap='gray')
            ax.quiver(xs, ys, us, vs, color='yellow', width=0.003, \
                        scale=scale, scale_units='width') # it's better to set a fixed scale, see *Analysis of Collective Motions in Droplets* Section IV.A.2 for more info.
            ax.axis('off')
            # save figure
            fig.savefig(os.path.join(out_folder, name + '.jpg'), dpi=dpi)

class fixed_mask_PIV:
    def PIV_masked_1(self, I0, I1, winsize, overlap, dt, mask):
        """Test different masking procedures.
        1. Mask raw images by setting background 0, then apply PIV.
        2. Mask raw images by setting background nan, then apply PIV.
        3. Apply PIV directly on raw images, then apply mask on velocity.
        """
        assert(mask.shape==I0.shape)
        mask = mask >= mask.mean() # convert mask to boolean array
        I0 = I0 * mask
        I1 = I1 * mask
        x, y, u, v = PIV(I0, I1, winsize, overlap, dt)
        mask_w = divide_windows(mask, windowsize=[winsize, winsize], step=winsize-overlap)[2] >= 1
        assert(mask_w.shape==x.shape)
        u[~mask_w] = np.nan
        v[~mask_w] = np.nan
        return x, y, u, v
    def PIV_masked_2(self, I0, I1, winsize, overlap, dt, mask):
        """Test different masking procedures.
        1. Mask raw images by setting background 0, then apply PIV.
        2. Mask raw images by setting background nan, then apply PIV.
        3. Apply PIV directly on raw images, then apply mask on velocity.
        """
        assert(mask.shape==I0.shape)
        mask = mask >= mask.mean() # convert mask to boolean array
        x, y, u, v = PIV(I0, I1, winsize, overlap, dt)
        mask_w = divide_windows(mask, windowsize=[winsize, winsize], step=winsize-overlap)[2] >= 1
        assert(mask_w.shape==x.shape)
        u[~mask_w] = np.nan
        v[~mask_w] = np.nan
        return x, y, u, v
    def PIV_masked_3(self, I0, I1, winsize, overlap, dt, mask):
        """Test different masking procedures.
        1. Mask raw images by setting background 0, then apply PIV.
        2. Mask raw images by setting background nan, then apply PIV.
        3. Apply PIV directly on raw images, then apply mask on velocity.
        """
        assert(mask.shape==I0.shape)
        mask = mask >= mask.mean() # convert mask to boolean array
        I0[~mask] = np.nan
        I1[~mask] = np.nan
        x, y, u, v = PIV(I0, I1, winsize, overlap, dt)
        mask_w = divide_windows(mask, windowsize=[winsize, winsize], step=winsize-overlap)[2] >= 1
        assert(mask_w.shape==x.shape)
        u[~mask_w] = np.nan
        v[~mask_w] = np.nan
        return x, y, u, v
    def test(self):
        I0 = io.imread(os.path.join("img", "I10.tif"))
        I1 = io.imread(os.path.join("img", "I11.tif"))
        mask = io.imread(os.path.join("img", "mask1.tif"))
        winsize = 40
        overlap = 20
        dt = 0.02
        x, y, u, v = [], [], [], []
        for func in [PIV_masked_1, PIV_masked_2]:
            x1, y1, u1, v1 = func(I0, I1, winsize, overlap, dt, mask)
            x.append(x1); y.append(y1); u.append(u1); v.append(v1)
        fig, ax = plt.subplots(nrows=1, ncols=2, dpi=200)
        for i in [0, 1]:
            ax[i].imshow(I0, cmap='gray')
            ax[i].quiver(x[i], y[i], u[i], v[i], color='yellow')
            ax[i].axis('off')
        print("The two masking procedures don't produce very different results, according to visual inspection.")
        print("I also plot the velocity distribution function below.")
        fig, ax = plt.subplots(nrows=1, ncols=2, dpi=200)
        for i in [0, 1]:
            hist, bin_edges = np.histogram(u[i][~np.isnan(u[i])], density=True)
            ax[0].plot(bin_edges[:-1], hist)
            hist, bin_edges = np.histogram(v[i][~np.isnan(v[i])], density=True)
            ax[1].plot(bin_edges[:-1], hist)
        ax[0].set_xlabel("u")
        ax[1].set_xlabel("v")
        ax[0].set_ylabel("PDF")
        print("The two methods show statistically very similar results")
        print("Test the speed of the two methods.")
        t = []
        t.append(time.monotonic())
        for func in [PIV_masked_1, PIV_masked_2]:
            x1, y1, u1, v1 = func(I0, I1, winsize, overlap, dt, mask)
            t.append(time.monotonic())
        t1 = t[1] - t[0]
        t2 = t[2] - t[1]
        plt.bar([1, 2], [t1, t2])
        plt.xticks([1, 2])
        plt.ylabel("time (s)")
        print("The second method takes longer time. So the first method is better.")
        print("Since it gives similar results while using less time.")
        I20 = io.imread(os.path.join("img", "I20.tif"))
        I21 = io.imread(os.path.join("img", "I21.tif"))
        mask2 = io.imread(os.path.join("img", "mask2.tif"))
        x, y, u, v = PIV_masked(I20, I21, 20, 10, 0.02, mask2)
        fig, ax = plt.subplots()
        ax.imshow(I20, cmap='gray')
        ax.quiver(x, y, u, v, color='yellow')
        ax.axis('off')

class de_data():
    """Double emulsion data plotting tool."""
    def __init__(self, data):
        self.data = data
    def __repr__(self):
        return(str(self.data))
    def show(self):
        print(self.data)
    def parameter_space(self, highlight_Chile_data=True):
        """D vs. d, with color coded OD"""
        # log1 = self.data.dropna(subset=["Rinfy", "t2"])
        log1 = self.data
        binsize = 10 # OD bin size
        plt.figure(figsize=(3.5,3),dpi=300)
        bin_starts = range(0, int(log1.OD.max()), binsize)
        cmap = plt.cm.get_cmap("tab10")
        for num, bs in enumerate(bin_starts):
            log2 = log1.loc[(log1.OD>bs)&(log1.OD<=bs+binsize)]
            if len(log2) == 0:
                continue
            if highlight_Chile_data == True:
                log3 = log2.loc[log2.Comment!="Chile"]
                log4 = log2.loc[log2.Comment=="Chile"]
                plt.scatter(log3.D, log3.d, color=cmap(num), label="{0:d}-{1:d}".format(bs,bs+binsize))
                plt.scatter(log4.D, log4.d, edgecolors=cmap(num), marker="^", fc=(0,0,0,0))
            else:
                plt.scatter(log2.D, log2.d, color=cmap(num), label="{0:d}-{1:d}".format(bs,bs+binsize))
        plt.xlabel("$D$ (um)")
        plt.ylabel("$d$ (um)")
        plt.xlim([0, 1.05*log1.D.max()])
        plt.ylim([0, 1.05*log1.d.max()])
        plt.plot([0, 1.05*log1.d.max()], [0, 1.05*log1.d.max()], ls=":", color="black")
        plt.legend(ncol=2, fontsize=5, loc="upper left")
    def generate_msd_repo(self, component="y", data_dir=r"..\Data\traj"):
        """Generate .jpg images for MSD repo. Takes ~2 min and save images, be careful!
        coord: the displacement component to compute, can be 'y' or 'z'.
        Edit:
        Mar 03, 2022 -- i) add z component, ii) put all DE# in image file name
        Mar 18, 2022 -- Use MPP info in log (Cristian's data are in um and is not consistent with this calculation.)"""
        mapper = {"y": "<y^2>", "z": "<x^2>"}
        log1 = self.data.dropna(subset=["OD"])
        if component == "z":
            log1 = log1.loc[log1.Plane=="XZ"]
        elif component == "y":
            pass
        else:
            raise ValueError("Invalid component, should be y or z")
        viridis = plt.cm.get_cmap('Set1', 5)
        count = 0
        plt.figure(dpi=150)
        name_list = []
        for num, i in log1.iterrows():
            traj_dir = os.path.join(data_dir, "{:02d}.csv".format(int(i["DE#"])))
            if os.path.exists(traj_dir):
                traj = pd.read_csv(traj_dir)
            else:
                print("Missing traj {:d}".format(i["DE#"]))
                continue
            msd = tp.msd(traj, mpp=i.MPP, fps=i.FPS, max_lagtime=traj.frame.max()//5).dropna()
            plt.plot(msd.lagt, msd[mapper[component]], label=i["DE#"], color=viridis(count/4))
            count += 1
            name_list.append("{:d}".format(int(i["DE#"])))
            if count > 4:
                plt.legend(fontsize=20, frameon=False)
                plt.xlabel("$\Delta t$ (s)")
                if component == "y":
                    plt.ylabel(r"$\left< \Delta y^2 \right>$ ($\mu$m$^2$)")
                elif component == "z":
                    plt.ylabel(r"$\left< \Delta z^2 \right>$ ($\mu$m$^2$)")
                plt.grid(which="both", ls=":")
                plt.loglog()
                plt.savefig("{}.jpg".format("-".join(name_list)))
                plt.figure(dpi=150)
                count = 0
                name_list = []
        plt.legend(fontsize=20, frameon=False)
        plt.xlabel("$\Delta t$ (s)")
        if component == "y":
            plt.ylabel(r"$\left< \Delta y^2 \right>$ ($\mu$m$^2$)")
        elif component == "z":
            plt.ylabel(r"$\left< \Delta z^2 \right>$ ($\mu$m$^2$)")
        plt.grid(which="both", ls=":")
        plt.loglog()
        plt.tight_layout()
        plt.savefig("{:d}.jpg".format(num))
    def scatter_0(self, mode="log", highlight_Chile_data=True):
        """Plot tau^* vs. (D-d)/d^2"""
        log1 = self.data.dropna(subset=["Rinfy", "t2"])
        binsize = 20 # OD bin size
        plt.figure(figsize=(3.5,3), dpi=100)
        bin_starts = range(0, int(log1.OD.max()), binsize)
        cmap = plt.cm.get_cmap("tab10")
        for num, bs in enumerate(bin_starts):
            log2 = log1.loc[(log1.OD>bs)&(log1.OD<=bs+binsize)]
            if highlight_Chile_data == True:
                log3 = log2.loc[log2.Comment!="Chile"]
                log4 = log2.loc[log2.Comment=="Chile"]
                plt.scatter(log3["(D-d)/d^2"], log3.t2_fit, color=cmap(num), label="{0:d}-{1:d}".format(bs,bs+binsize))
                plt.scatter(log4["(D-d)/d^2"], log4.t2_fit, edgecolors=cmap(num), marker="^", fc=(0,0,0,0))
            else:
                plt.scatter(log2["(D-d)/d^2"], log2.t2_fit, color=cmap(num), label="{0:d}-{1:d}".format(bs,bs+binsize))
        plt.xlabel("$(D-d)/d^2$")
        plt.ylabel("$\\tau^*$ (s)")
        plt.legend(ncol=2, fontsize=6)
        plt.grid(which="both", ls=":")
        if mode == "log":
            plt.loglog()
    def look_for_missing_traj(self, traj_folder, fmt="{:02d}.csv"):
        """Check the existence of trajectory data file in given folder, according to the log"""
        log1 = self.data.dropna(subset=["OD"])
        n_missing = 0
        for num, i in log1.iterrows():
            traj_dir = os.path.join(traj_folder, fmt.format(int(i["DE#"])))
            if os.path.exists(traj_dir):
                traj = pd.read_csv(traj_dir)
            else:
                print("Missing traj {:d}".format(i["DE#"]))
                n_missing += 1
        print("{:d} trajectories are missing".format(n_missing))
    def plot_MSD_model_Cristian(self):
        """plot the MSD model, get a feeling of parameters, save for future use, not finished"""
        gamma = 2
        nu = 1
        t = np.logspace(-2, 2)
        y2 = (1 - np.exp(-2*gamma*t)) / (2*gamma) - (np.exp(-(gamma+nu)*t)-np.exp(-2*gamma*t))
        gamma = 0.5
        y3 = (1 - np.exp(-2*gamma*t)) / (2*gamma) - (np.exp(-(gamma+nu)*t)-np.exp(-2*gamma*t))
        plt.figure(figsize=(3.5, 3), dpi=100)
        plt.plot(t, y2, label="$\\tau=1, \\tau^*=0.5$")
        plt.plot(t, y3, label="$\\tau=1, \\tau^*=2$")
        plt.legend()
        plt.loglog()
        plt.grid(which="both", ls=":")
        plt.xlabel("lag time")
        plt.ylabel("$\left<\Delta y^2\\right>$")
    def plot_0(self, nbins=5, overlap=0, mode="log"):
        """tau vs. (D-d)/d^2, with average"""
        log = self.data
        xm = 0
        ym = 0
        cmap = plt.cm.get_cmap("tab10")
        plt.figure(figsize=(3.5,3), dpi=100)
        for num, OD_min in enumerate(range(0, 160, 20)):
            OD_max = OD_min + 20
            log1 = log.loc[(log.OD>=OD_min)&(log.OD<=OD_max)].dropna(subset=["Rinfy"])
            r = (log1.D - log1.d) / log1.d ** 2
            # visualize the bins
            # plt.figure(dpi=100)
            # plt.scatter(r, log1["DE#"])
            # for num, i in log1.iterrows():
            #     plt.annotate(i["DE#"], ((i.D - i.d) / i.d ** 2, i["DE#"]), xycoords="data")
            # plt.xlabel("$(D-d)/d^2$")
            # plt.ylabel("DE index")
            if mode == "log":
                bins = np.logspace(np.log(r.min()), np.log(r.max()), nbins+1)
            else:
                bins = np.linspace(r.min(), r.max(), nbins+1)
            bin_start = bins[:-1]
            bin_size = bins[1:] - bins[:-1]
            bin_end = bin_start + bin_size * (1 + overlap)
            # count = 20
            # for start, end in zip(bin_start, bin_end):
            #     plt.plot([start, end], [count, count])
            #     count += 2
            # plot Rinf as a function of B
            count = 0
            for start, end in zip(bin_start, bin_end):
                log2 = log1.loc[(r>=start)&(r<=end)]
                r2 = (log2.D - log2.d) / log2.d ** 2
                x = r2.mean()
                y =(log2.t2).mean()
                xe = r2.std()
                ye = (log2.t2).std()
                if count == 0:
                    plt.errorbar(x, y, xerr=xe, yerr=ye, marker="o", color=cmap(num), label="{0:d}-{1:d}".format(OD_min, OD_max))
                    count += 1
                else:
                    plt.errorbar(x, y, xerr=xe, yerr=ye, marker="o", color=cmap(num))
                if np.isnan(xe):
                    xe = 0
                if np.isnan(ye):
                    ye = 0
                if x + xe > xm:
                    xm = x + xe
                if y + ye > ym:
                    ym = y + ye
        plt.xlabel("$(D-d)/d^2$")
        plt.ylabel("$\\tau^*$ (s)")
        plt.legend(ncol=2, fontsize=6, loc="lower right")
        if mode == "log":
            plt.loglog()
            plt.grid(which="both", ls=":")
        else:
            plt.xlim([0, xm*1.1])
            plt.ylim([0, ym*1.1])
    def scatter_1(self, mode="log", highlight_Chile_data=True):
        """R_inf vs. (D-d)/d^2"""
        log1 = self.data.dropna(subset=["Rinfy", "t2"])
        binsize = 20 # OD bin size
        plt.figure(figsize=(3.5,3), dpi=100)
        bin_starts = range(0, int(log1.OD.max()), binsize)
        cmap = plt.cm.get_cmap("tab10")
        for num, bs in enumerate(bin_starts):
            log2 = log1.loc[(log1.OD>bs)&(log1.OD<=bs+binsize)]
            if highlight_Chile_data == True:
                log3 = log2.loc[log2.Comment!="Chile"]
                log4 = log2.loc[log2.Comment=="Chile"]
                plt.scatter(log3["(D-d)/d^2"], log3.Rinfy**0.5, color=cmap(num), label="{0:d}-{1:d}".format(bs,bs+binsize))
                plt.scatter(log4["(D-d)/d^2"], log4.Rinfy**0.5, edgecolors=cmap(num), marker="^", fc=(0,0,0,0))
            else:
                plt.scatter(log2["(D-d)/d^2"], log2.Rinfy**0.5, color=cmap(num), label="{0:d}-{1:d}".format(bs,bs+binsize))
        plt.xlabel("$(D-d)/d^2$")
        plt.ylabel("$R_\infty$ (um)")
        plt.legend(ncol=2, fontsize=6)
        plt.grid(which="both", ls=":")
        if mode == "log":
            plt.loglog()
    def plot_1(self, nbins=5, overlap=0, mode="log"):
        """R_inf vs. (D-d)/d^2, with average"""
        log = self.data
        xm = 0
        ym = 0
        cmap = plt.cm.get_cmap("tab10")
        plt.figure(figsize=(3.5,3), dpi=100)
        for num, OD_min in enumerate(range(0, 160, 20)):
            OD_max = OD_min + 20
            log1 = log.loc[(log.OD>=OD_min)&(log.OD<=OD_max)].dropna(subset=["Rinfy"])
            r = (log1.D - log1.d) / log1.d ** 2
            # visualize the bins
            # plt.figure(dpi=100)
            # plt.scatter(r, log1["DE#"])
            # for num, i in log1.iterrows():
            #     plt.annotate(i["DE#"], ((i.D - i.d) / i.d ** 2, i["DE#"]), xycoords="data")
            # plt.xlabel("$(D-d)/d^2$")
            # plt.ylabel("DE index")
            if mode == "log":
                bins = np.logspace(np.log(r.min()), np.log(r.max()), nbins+1)
            else:
                bins = np.linspace(r.min(), r.max(), nbins+1)
            bin_start = bins[:-1]
            bin_size = bins[1:] - bins[:-1]
            bin_end = bin_start + bin_size * (1 + overlap)
            # count = 20
            # for start, end in zip(bin_start, bin_end):
            #     plt.plot([start, end], [count, count])
            #     count += 2
            # plot Rinf as a function of B
            count = 0
            for start, end in zip(bin_start, bin_end):
                log2 = log1.loc[(r>=start)&(r<=end)]
                r2 = (log2.D - log2.d) / log2.d ** 2
                x = r2.mean()
                y =(log2.Rinfy**0.5).mean()
                xe = r2.std()
                ye = (log2.Rinfy**0.5).std()
                if count == 0:
                    plt.errorbar(x, y, xerr=xe, yerr=ye, marker="o", color=cmap(num), label="{0:d}-{1:d}".format(OD_min, OD_max))
                    count += 1
                else:
                    plt.errorbar(x, y, xerr=xe, yerr=ye, marker="o", color=cmap(num))
                if np.isnan(xe):
                    xe = 0
                if np.isnan(ye):
                    ye = 0
                if x + xe > xm:
                    xm = x + xe
                if y + ye > ym:
                    ym = y + ye
        plt.xlabel("$(D-d)/d^2$")
        plt.ylabel("$R_\infty$ (um)")
        plt.legend(ncol=2, fontsize=6, loc="lower right")
        if mode == "log":
            plt.loglog()
            plt.grid(which="both", ls=":")
        else:
            plt.xlim([0, xm*1.1])
            plt.ylim([0, ym*1.1])
    def Rinf2_tau(self):
        """Plot $R_\infty^2$ vs. $\tau^*$"""
        log = self.data
        log1 = log.dropna(subset=["Rinfy", "t2"])
        binsize = 20 # OD bin size
        plt.figure(figsize=(3.5,3), dpi=100)
        bin_starts = range(0, int(log1.OD.max()), binsize)
        cmap = plt.cm.get_cmap("tab10")
        for num, bs in enumerate(bin_starts):
            log2 = log1.loc[(log1.OD>bs)&(log1.OD<=bs+binsize)]
            log3 = log2.loc[log2.Comment!="Chile"]
            log4 = log2.loc[log2.Comment=="Chile"]
            plt.scatter(log3.t2, log3.Rinfy, color=cmap(num), label="{0:d}-{1:d}".format(bs,bs+binsize))
            plt.scatter(log4.t2, log4.Rinfy, edgecolors=cmap(num), marker="^", fc=(0,0,0,0))
        plt.xlabel("$\\tau^*$ (s)")
        plt.ylabel("$R_\infty^2 $ (um$^2$)")
        plt.legend(ncol=2, fontsize=6, loc="lower right")
        plt.grid(which="both", ls=":")
        plt.xlim([1, 30])
        plt.loglog()
    def Rinf2_over_tau(self, x="(D-d)/d^2", ax=None, xlabel=None):
        """Plot $R_\infty^2 / \tau^*$ vs. $(D-d)/d^2$
        Edit:
        05032022 -- add custom x-axis"""
        log = self.data
        log1 = log.dropna(subset=["Rinfy", "t2"])
        binsize = 20 # OD bin size
        if ax == None:
            fig, ax = plt.subplots(figsize=(3.5,3), dpi=100)
        bin_starts = range(0, int(log1.OD.max()), binsize)
        cmap = plt.cm.get_cmap("tab10")
        for num, bs in enumerate(bin_starts):
            log2 = log1.loc[(log1.OD>bs)&(log1.OD<=bs+binsize)]
            log3 = log2.loc[log2.Comment!="Chile"]
            log4 = log2.loc[log2.Comment=="Chile"]
            ax.scatter(log3[x], log3.Rinfy/(log3.t2), color=cmap(num), label="{0:d}-{1:d}".format(bs,bs+binsize))
            ax.scatter(log4[x], log4.Rinfy/(log4.t2), edgecolors=cmap(num), marker="^", fc=(0,0,0,0))
        if xlabel == None:
            xlabel = x
        ax.set_xlabel("${}$".format(xlabel))
        ax.set_ylabel("$R_\infty^2 / \\tau^*$")
        ax.legend(ncol=2, fontsize=6, loc="lower right")
        ax.grid(which="both", ls=":")
        ax.loglog()
    def rescale_Rinf_OD(self):
        """Plot Rinf/OD vs. (D-d)/d^2"""
        log = self.data
        log1 = log.dropna(subset=["Rinfy", "t2"])
        binsize = 20 # OD bin size
        plt.figure(figsize=(3.5,3), dpi=100)
        bin_starts = range(0, int(log1.OD.max()), binsize)
        cmap = plt.cm.get_cmap("tab10")
        for num, bs in enumerate(bin_starts):
            log2 = log1.loc[(log1.OD>bs)&(log1.OD<=bs+binsize)]
            log3 = log2.loc[log2.Comment!="Chile"]
            log4 = log2.loc[log2.Comment=="Chile"]
            plt.scatter(log3["(D-d)/d^2"], log3.Rinfy**0.5/(log3.OD), color=cmap(num), label="{0:d}-{1:d}".format(bs,bs+binsize))
            plt.scatter(log4["(D-d)/d^2"], log4.Rinfy**0.5/(log4.OD), edgecolors=cmap(num), marker="^", fc=(0,0,0,0))
        plt.xlabel("$(D-d)/d^2$")
        plt.ylabel("$R_\infty / OD$")
        plt.legend(ncol=2, fontsize=6)
        plt.grid(which="both", ls=":")
        plt.loglog()
    def rescale_Rinf_freespace(self):
        # rescale Rinf with (D-d)
        log = self.data
        log1 = log.dropna(subset=["Rinfy", "t2"])
        binsize = 20 # OD bin size
        plt.figure(figsize=(3.5, 3), dpi=100)
        bin_starts = range(0, int(log1.OD.max()), binsize)
        cmap = plt.cm.get_cmap("tab10")
        for num, bs in enumerate(bin_starts):
            log2 = log1.loc[(log1.OD>bs)&(log1.OD<=bs+binsize)]
            log3 = log2.loc[log2.Comment!="Chile"]
            log4 = log2.loc[log2.Comment=="Chile"]
            plt.scatter(log3["(D-d)/d^2"], log3.Rinfy**0.5/(log3.D-log3.d), color=cmap(num), label="{0:d}-{1:d}".format(bs,bs+binsize))
            plt.scatter(log4["(D-d)/d^2"], log4.Rinfy**0.5/(log4.D-log4.d), edgecolors=cmap(num), marker="^", fc=(0,0,0,0))
        plt.xlabel("$(D-d)/d^2$")
        plt.ylabel("$R_\infty / (D-d)$")
        plt.legend(ncol=2, fontsize=6)
        plt.grid(which="both", ls=":")
        plt.loglog()
    def scatter(self, x="D-d", y="DA_fit", xlabel=None, ylabel=None, ax=None, mode="log", highlight_Chile_data=True):
        """I want to implement a more flexible plotting tool to test ideas.
        The data will still be plotted in OD bins of 20. The args allow one to specify which column(s) to plot,
        and what label(s) to use for the xy-axes.
        Edit:
        05172022 -- Initial commit."""
        log1 = self.data
        # log1 = log.dropna(subset=["Rinfy", "t2"])
        binsize = 10 # OD bin size
        if ax == None:
            fig, ax = plt.subplots(figsize=(3.5,3), dpi=300)
        bin_starts = range(0, int(log1.OD.max()), binsize)
        cmap = plt.cm.get_cmap("tab10")
        for num, bs in enumerate(bin_starts):
            log2 = log1.loc[(log1.OD>bs)&(log1.OD<=bs+binsize)]
            if len(log2) == 0:
                continue
            log3 = log2.loc[log2.Comment!="Chile"]
            log4 = log2.loc[log2.Comment=="Chile"]
            if highlight_Chile_data == True:
                ax.scatter(log3[x], log3[y], color=cmap(num), label="{0:d}-{1:d}".format(bs,bs+binsize))
                ax.scatter(log4[x], log4[y], edgecolors=cmap(num), marker="^", fc=(0,0,0,0))
            else:
                ax.scatter(log2[x], log2[y], color=cmap(num), label="{0:d}-{1:d}".format(bs,bs+binsize))
        if xlabel == None:
            xlabel = x
        if ylabel == None:
            ylabel = y
        ax.set_xlabel("{}".format(xlabel))
        ax.set_ylabel("{}".format(ylabel))
        ax.legend(ncol=1, fontsize=6, loc="upper left")
        if mode == "log":
            ax.grid(which="both", ls=":")
            ax.loglog()
        return ax

class drop_data:
    """Droplet data plotting tool."""
    def __init__(self, data):
        """Initialize a data object with main log spreadsheet (pd.DataFrame)"""
        self.data = data
        self.OD_to_nc = 8e8 # OD to number concentration conversion factor, cells/ml
        self.single_bacterial_volume = 1 # um^3
    def __repr__(self):
        return self.data.__repr__()
    def parameter_space(self):
        """Plot the parameter space of current data, D vs. OD"""
        fig, ax = plt.subplots(figsize=(3.5, 3), dpi=100)
        ax.scatter(self.data["Bacterial concentration"], self.data["Droplet size"])
        ax.set_xlabel("OD")
        ax.set_ylabel("$D$ (um)")
    def find_lifetime_data(self, n=5):
        """Return the Droplet#'s of droplets with more than n videos, n is 5 by default"""
        self.lifetime_data_list = []
        for i in self.data["Droplet#"].drop_duplicates():
            subdata = self.data.loc[self.data["Droplet#"]==i]
            if len(subdata) >= n:
                self.lifetime_data_list.append(i)
        # print("Lifetime data located: {}".format(str(self.lifetime_data_list)))
    def plot_mean_velocity_evolution(self, n=5, mode="log"):
        """Plot mean velocity vs. time.
        Use the time of first video as 0 (or 1 in log mode)
        n: number of curves on each plot
        mode: the scale of time axis, can be 'lin' or 'log' (default)"""
        self.find_lifetime_data()
        cmap = plt.cm.get_cmap("Set1")
        for num, i in enumerate(self.lifetime_data_list):
            if num % n == 0:
                fig, ax = plt.subplots(figsize=(3.5, 2), dpi=100)
                ax.set_xlabel("time (min)")
                ax.set_ylabel("mean velocity (um/s)")
                ax.set_xlim([0, 60])
                if mode == "log":
                    ax.set_xlim([1, 60])
                    ax.set_xscale("log")
                ax.set_ylim([0, 15])
            subdata = self.data.loc[self.data["Droplet#"]==i]
            t = subdata["Time in minutes"]
            t -= subdata["Time in minutes"].min()
            v = subdata["Initial mean velocity (10 s)"]
            if mode == "log":
                t += 1
            ax.plot(t, v, marker="s", color=cmap(num % n), label="{:d}".format(i))
            ax.legend(frameon=False)
    def plot_droplet_size_evolution(self, n=5, mode="log"):
        """Plot droplet size vs. time.
        Use the time of first video as 0 (or 1 in log mode)
        n: number of curves on each plot
        mode: the scale of time axis, can be 'lin' or 'log' (default)"""
        self.find_lifetime_data()
        cmap = plt.cm.get_cmap("Set1")
        for num, i in enumerate(self.lifetime_data_list):
            if num % n == 0:
                fig, ax = plt.subplots(figsize=(3.5, 2), dpi=100)
                ax.set_xlabel("time (min)")
                ax.set_ylabel("droplet diameter (um)")
                ax.set_xlim([0, 60])
                if mode == "log":
                    ax.set_xlim([1, 60])
                    ax.set_xscale("log")
                if mode == "loglog":
                    ax.set_xlim([1, 60])
                    ax.set_xscale("log")
                    ax.set_yscale("log")
                # ax.set_ylim([0, 15])
            subdata = self.data.loc[self.data["Droplet#"]==i]
            t = subdata["Time in minutes"]
            t -= subdata["Time in minutes"].min()
            D = subdata["Droplet size"]
            if mode == "log":
                t += 1
            ax.plot(t, D, marker="s", color=cmap(num % n), label="{:d}".format(i))
            ax.legend(frameon=False)
    def plot_volume_fraction_evolution(self, n=5, mode="log"):
        """Plot droplet size vs. time.
        Use the time of first video as 0 (or 1 in log mode)
        n: number of curves on each plot
        mode: the scale of time axis, can be 'lin' or 'log' (default)"""
        self.find_lifetime_data()
        cmap = plt.cm.get_cmap("Set1")

        for num, i in enumerate(self.lifetime_data_list):
            if num % n == 0:
                fig, ax = plt.subplots(figsize=(3.5, 2), dpi=100)
                ax.set_xlabel("time (min)")
                ax.set_ylabel("volume fraction")
                ax.set_xlim([0, 60])
                if mode == "log":
                    ax.set_xlim([1, 60])
                    ax.set_xscale("log")
                ax.set_ylim([0.1, 0.3])
            subdata = self.data.loc[self.data["Droplet#"]==i]
            initial_droplet_volume = 4/3 * np.pi * (subdata["Droplet size"].iloc[0]/2) ** 3
            bacterial_volume = subdata["Bacterial concentration"].iloc[0] * self.OD_to_nc * initial_droplet_volume * 1e-12 * self.single_bacterial_volume

            t = subdata["Time in minutes"]
            t -= subdata["Time in minutes"].min()
            vf = bacterial_volume / (4/3 * np.pi * (subdata["Droplet size"]/2) ** 3)
            if mode == "log":
                t += 1
            ax.plot(t, vf, marker="s", color=cmap(num % n), label="{:d}".format(i))
            ax.legend(frameon=False)
    def plot_velocity_volume_fraction_correlation(self, time_bins=5):
        """Plot the correlation between mean velocity and volume fraction
        time_bins: number of time bins"""
        self.find_lifetime_data()
        cmap = plt.cm.get_cmap("Set1")
        bin_size = 60 // time_bins
        bin_starts = range(0, 60, bin_size)
        plot_data_list = []
        for num, i in enumerate(self.lifetime_data_list):
            subdata = self.data.loc[self.data["Droplet#"]==i]
            initial_droplet_volume = 4/3 * np.pi * (subdata["Droplet size"].iloc[0]/2) ** 3
            bacterial_volume = subdata["Bacterial concentration"].iloc[0] * self.OD_to_nc * initial_droplet_volume * 1e-12 * self.single_bacterial_volume
            t = subdata["Time in minutes"]
            t -= subdata["Time in minutes"].min()
            vf = bacterial_volume / (4/3 * np.pi * (subdata["Droplet size"]/2) ** 3)
            plot_data = subdata.assign(t=t, vf=vf)
            plot_data_list.append(plot_data)
        data = pd.concat(plot_data_list, axis=0)
        fig, ax = plt.subplots(figsize=(3.5, 3), dpi=100)
        for num, start in enumerate(bin_starts):
            subdata = data.loc[(data.t>start)&(data.t<=start+bin_size)]
            ax.scatter(subdata.vf, subdata["Initial mean velocity (10 s)"],
                       color=cmap(num), label="{0:.0f}-{1:.0f}".format(start, start+bin_size))
        ax.set_xlabel("volume fraction")
        ax.set_ylabel("mean velocity")
        ax.legend()

def subpixel_correction(original_circle, raw_img, range_factor=0.5, plot=False, thres=5, method="gaussian", sample=5, sample_range=(0, 2*np.pi), ax=None):
    """Use gaussian fitting of cross-boundary pixel intensities to give circle detections subpixel accuracy. 
    Args:
    original_circle -- dict of {"x", "y", "r"}
    raw_img -- raw image where circles are detected
    range_factor -- the range of the cross-boundary pixel intensity profile to be fitted.
                    For example, 0.6 means 0.6*r on both sides of the boundary pixel (in and out of the circle, 1.2*r in total)".
    Returns:
    corrected_circle -- dict of {"x", "y", "r"}
    Edit:
    06152022 -- Initial commit.
    06162022 -- If the peak value is too far away from the original one, drop it.
    06172022 -- 1) add boundary protection,
                2) use gaussian smoothing, instead of savgol
                3) convert pixel data type to "float64" to avoid memory overflow
                4) put fitting part together
                5) merge gaussian and minimum fitting in the same function, adding "method" argument, change name to subpixel_correction
    06212022 -- Sample more profiles for more accurate correction.
                Note that sometimes more profiles does not mean more accuracy.
                If the outer droplet boundary is very dark, 
                and some profiles contain the outer droplet boundary,
                significant deviation will result.
    06282022 -- Add argument "sample_range".
                In most DE images, the upper boundary of inner and outer droplets overlap.
                As a result, when sampling across the upper boundaries, the profile will likely include both boundaries.
                This leads to big error for the "minimum" method.
                Therefore, it is desired to sample bottom boundaries.
                sample_range allows specifying the range of boundary samples (in terms of angle).
                The x-axis corresponds to 0 in sample_range. Then it increases in the CW direction.
                Up to 2*np.pi where it comes back to the x-axis.
    07132022 -- Use linear method for circle fitting, for better efficiency and less susceptibility to outliers.
    07192022 -- i) Back to "naive" fitting
                ii) Add cross-boundary lines, chosen peaks on the profiles, fitted corrected circles to plot
                iii) add argument ax for making subplots outside the function
                iv) set default of plot param to False
    """
    
    
    if ax == None and plot:
        fig, ax = plt.subplots(dpi=150)
    if plot:
        ax.imshow(raw_img, cmap="gray")
        
    x0, y0, r0 = original_circle["x"], original_circle["y"], original_circle["r"]
    # samples
    new_points = []
    for t in np.linspace(*sample_range, sample, endpoint=True):
        xc = x0 + r0 * np.cos(t)
        yc = y0 + r0 * np.sin(t)
        x1 = xc - r0 * range_factor * np.cos(t)
        x2 = xc + r0 * range_factor * np.cos(t)
        y1 = yc - r0 * range_factor * np.sin(t)
        y2 = yc + r0 * range_factor * np.sin(t)
        x1 = int(np.round(x1))
        x2 = int(np.round(x2))
        y1 = int(np.round(y1))
        y2 = int(np.round(y2))
        
        y, x = draw.line(y1, x1, y2, x2)
        if plot:
            ax.plot(x, y, color="yellow")
        indx = (x >= 0) & (x < raw_img.shape[1])
        indy = (y >= 0) & (y < raw_img.shape[0])
        ind = indx * indy
        y = y[ind]
        x = x[ind]
        p = raw_img[y, x]
        p_smooth = gaussian_filter1d(p, sigma=3/4)
        if method == "minimum":
            minind = np.argmin(p_smooth)
            xmin, ymin = x[minind], y[minind]
            distsq = (xmin - xc) ** 2 + (ymin - yc) ** 2 
            if distsq > thres ** 2:
                new_points.append((xc, yc))
            else:
                new_points.append((xmin, ymin))
        elif method == "gaussian":
            raise ValueError("Method not yet implemented")
            
    # fit circle
    xy = np.array(new_points)
    c, n_iter = fit_circle(xy[:, 0], xy[:, 1], method="naive")
    corrected_circle = {"x": c["a"], "y": c["b"], "r": c["r"]}
    
    if plot:
        points = np.array(new_points)
        ax.scatter(points[:, 0], points[:, 1], s=10, color="red")
        ocirc = mpatch.Circle((x0, y0), r0, fill=False, color="red", lw=1)
        ax.add_patch(ocirc)
        ccirc = mpatch.Circle((c["a"], c["b"]), c["r"], fill=False, color="green", lw=1)
        ax.add_patch(ccirc)
        
    return corrected_circle

def circle_quality_std(raw_img, circle):
    """Quantify circle detection quality by computing boundary pixel standard deviation.
    Args:
    raw_img -- raw image
    circle -- dict of {"x", "y", "r"}
    distsq_thres -- distance threshold for determining if a pixel is on a circle or not
    Returns:
    quality -- 1 - (circle pixel std) / (image pixel std)
                The idea is to normalize the results from images of different contrast,
                and larger quality value means better tracking.
    Edit:
    06282022 -- use skimage.draw to get circle perimeter pixel coords
    """
    x, y, r = circle["x"], circle["y"], circle["r"]
    # 1. make X, Y coordinates of all image pixels
    Y, X = np.mgrid[0:raw_img.shape[0], 0:raw_img.shape[1]]
    # 2. compute distance (square) matrix from each pixel to circle center
    dist = (X-x) ** 2 + (Y-y) ** 2 - r ** 2 
    # 3. get all the pixel intensity values on the detected circle
    circle_pixels = raw_img[draw.circle_perimeter(int(np.round(y)), int(np.round(x)), int(np.round(r)), shape=raw_img.shape)]
    # 4. compute standard deviation of circle_pixels
    std = circle_pixels.std()
    std_img = raw_img.std()
    
    return 1 - std / std_img