import matplotlib.pyplot as plt
import numpy as np
from sklearn.manifold import TSNE
from sklearn.preprocessing import MinMaxScaler


def visualize_embeddings(X, dims=2, fname="tsne_embedding"):
    """
    Given a numpy array of images X, flatten the images
    and plot a 2D or 3D embedding using t-SNE.

    Parameters:
    X (numpy array): Array of images of shape (num_images, height, width, channels)
                     or (num_images, height, width) for grayscale images.
    dims (int): Number of dims for t-SNE embedding (2 or 3).

    Returns:
    embedding (numpy array): The 2D or 3D embedding.
    """

    if dims not in [2, 3]:
        raise ValueError("dims parameter must be 2 or 3.")

    # Get number of images and flatten each image
    num_images = X.shape[0]
    image_size = np.prod(
        X.shape[1:]
    )  # height * width * channels (or height * width for grayscale)
    flat_images = X.reshape(num_images, image_size)

    # Apply t-SNE to reduce dimensionality to 2D or 3D
    tsne = TSNE(n_components=dims, random_state=42)
    embedding = tsne.fit_transform(flat_images)
    embedding = MinMaxScaler().fit_transform(embedding)

    # Plot the embedding
    plt.figure(figsize=(8, 6))

    if dims == 2:
        plt.scatter(embedding[:, 0], embedding[:, 1], s=5, c="black")
        plt.title("2D Embedding of Images using t-SNE")
        plt.xlabel("Dimension 1")
        plt.ylabel("Dimension 2")

    elif dims == 3:
        ax = plt.axes(projection="3d")
        ax.scatter(embedding[:, 0], embedding[:, 1], embedding[:, 2], s=5, c="black")
        ax.set_title("3D Embedding of Images using t-SNE")
        ax.set_xlabel("Dimension 1")
        ax.set_ylabel("Dimension 2")
        ax.set_zlabel("Dimension 3")

    plt.show()
    plt.savefig(f"examples/{dims}d_{fname}.png", dpi=300)

    return embedding
