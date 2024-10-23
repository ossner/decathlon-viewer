import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium", app_title="Dataviewer")


@app.cell
def __():
    import marimo as mo
    import nibabel as nib
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.colors import Normalize
    from io import BytesIO
    from PIL import Image
    import os
    return BytesIO, Image, Normalize, mo, nib, np, os, plt


@app.cell
def __(BytesIO, Image, Normalize, nib, np, plt, sliderAlph):
    def load_nii(file_path):
        img = nib.load(file_path)
        return img.get_fdata()

    def load_image(image, label):
        # Normalize the image for better visualization
        norm = Normalize(vmin=np.min(image), vmax=np.max(image))
        image = norm(image)

        overlays = []

        # Iterate through slices and create overlays
        for slice_idx in range(image.shape[2]):
            fig, ax = plt.subplots()
            ax.imshow(image[:, :, slice_idx], cmap="gray")
            ax.imshow(label[:, :, slice_idx], cmap="jet", alpha=sliderAlph.value)
            ax.axis('off')

            # Save the plot to memory (BytesIO) instead of displaying it
            buf = BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
            buf.seek(0)

            # Convert the buffer to an image (PIL Image)
            overlay_image = Image.open(buf)
            overlays.append(overlay_image)

            plt.close(fig)  # Close the plot to free memory

        return overlays
    return load_image, load_nii


@app.cell
def __(dropdownDir, dropdownImg, load_image, load_nii):
    image_file = f'data/{dropdownDir.value}/imagesTr/{dropdownImg.value}'
    label_file = f'data/{dropdownDir.value}/labelsTr/{dropdownImg.value}'

    image_data = load_nii(image_file)
    label_data = load_nii(label_file)

    overlays = load_image(image_data, label_data)
    return image_data, image_file, label_data, label_file, overlays


@app.cell
def __(mo, os):
    _organDirs = list(filter(lambda x: os.path.isdir(os.path.join('data/', x)), sorted(os.listdir('data/'))))
    mo.stop(len(_organDirs) == 0, mo.md('**ERROR:** *data directory does not have subdirectories*'))
    dropdownDir = mo.ui.dropdown(
        options=_organDirs, value=_organDirs[0], label="Choose Organ"
    )
    return (dropdownDir,)


@app.cell
def __(dropdownDir, mo, os):
    _organIms = list(filter(lambda x: x.endswith('.nii.gz'), os.listdir(f'data/{dropdownDir.value}/imagesTr/')))
    dropdownImg = mo.ui.dropdown(
        options=_organIms, value=_organIms[0], label="Choose Image"
    )
    return (dropdownImg,)


@app.cell
def __(mo, overlays):
    sliderSlc = mo.ui.slider(start=0, stop=len(overlays) - 1, step=1, label="Slice")
    return (sliderSlc,)


@app.cell
def __(mo):
    sliderAlph = mo.ui.slider(start=0, stop=1, step=0.05, value=0.2, label="Overlay alpha (requires reload)")
    return (sliderAlph,)


@app.cell
def __(dropdownDir, dropdownImg, mo, sliderAlph, sliderSlc):

    mo.vstack([dropdownDir, dropdownImg, sliderSlc, sliderAlph])
    return


@app.cell
def __(overlays, plt, sliderSlc):
    plt.figure(figsize=(8, 8))
    plt.imshow(overlays[sliderSlc.value])
    plt.axis('off')
    plt.gca()
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
