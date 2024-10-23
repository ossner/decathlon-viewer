import marimo

__generated_with = "0.8.0"
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
def __(BytesIO, Image, Normalize, nib, np, plt):
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
            ax.imshow(label[:, :, slice_idx], cmap="jet", alpha=0.2)
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
    dropdownDir = mo.ui.dropdown(
        options=sorted(os.listdir('data/')), value="Task07_Pancreas", label="Choose Organ"
    )
    return dropdownDir,


@app.cell
def __(dropdownDir, mo, os):
    dropdownImg = mo.ui.dropdown(
        options=sorted(os.listdir(f'data/{dropdownDir.value}/imagesTr/')), value=sorted(os.listdir(f'data/{dropdownDir.value}/imagesTr/'))[0], label="Choose Image"
    )
    return dropdownImg,


@app.cell
def __(mo, overlays):
    slider = mo.ui.slider(start=0, stop=len(overlays) - 1, step=1)
    return slider,


@app.cell
def __(dropdownDir, dropdownImg, mo, slider):
    mo.vstack([dropdownDir, dropdownImg, slider])
    return


@app.cell
def __(overlays, plt, slider):
    plt.figure(figsize=(8, 8))
    plt.imshow(overlays[slider.value])
    plt.axis('off')
    plt.gca()
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
