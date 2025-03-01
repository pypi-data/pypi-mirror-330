import numpy as np
from pylibCZIrw import czi as pyczi

def save_numpy_as_czi(array, output_path):
    """
    Save a 5D NumPy array (T, C, Z, Y, X) as a CZI file.

    Args:
        array (np.ndarray): The 5D NumPy array (T, C, Z, Y, X) to save.
        output_path (str): Path to save the CZI file.

    Returns:
        None
    """
    try:
        # Extract dimensions
        T, C, Z, Y, X = array.shape

        with pyczi.create_czi(output_path) as czidoc_w:
            # Write each frame, channel, and slice into the CZI file
            for t in range(T):
                for c in range(C):
                    for z in range(Z):
                        # Extract and write the slice data
                        slice_data = array[t, c, z, :, :].astype(np.float32)  # Ensure correct dtype
                        czidoc_w.write(
                            data=slice_data,
                            plane={"T": t, "C": c, "Z": z},
                            scene=0  # Assuming a single scene
                        )

            # Write metadata with default scaling
            metadata = {
                "document_name": "Processed Image",
                "scale_x": 0.1 * 10 ** -6,  # Example scaling in meters
                "scale_y": 0.1 * 10 ** -6,
                "scale_z": 0.3 * 10 ** -6,  # Adjust scaling as per your dataset
            }
            czidoc_w.write_metadata(**metadata)

        print(f"Saved processed data as CZI: {output_path}")

    except Exception as e:
        print(f"Error saving CZI file: {e}")

