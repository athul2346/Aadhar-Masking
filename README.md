# Aadhar Masking Tool
# Overview

Aadhar masking is a crucial step for financial companies to comply with RBI rules when storing Aadhar images of their customers. This tool is designed to automatically mask Aadhar card images by drawing a rectangle over the first 8 digits. The implementation leverages Google's Vision API for accurate text extraction, achieving approximately 95% accuracy in detecting Aadhar numbers.
# Prerequisites

Before using this tool, ensure that you have a valid Google Vision API JSON key, as the code relies on the API for text extraction.
# Usage

    Image Conversion: The tool begins by converting all images in the specified input folder to JPEG format. These images are then moved to the output folder.

    Aadhar Masking: The code scans each image for Aadhar card numbers using regular expressions. If found, it masks the first 8 digits by drawing a rectangle over them. If an Aadhar number is not detected, the tool checks whether the image is an Aadhar card. If so, the image is moved to the output folder, assuming it is already masked.

    Handling Unreadable Images: In cases where the Vision API fails to read an image, the tool moves the image to the "unmasked" folder since masking cannot be applied.

# Folder Structure

Ensure that your directory structure includes the following folders:

    input: Contains the original images to be masked.
    realinput: Holds the images recognized as Aadhar cards after processing.
    output: Stores the masked images.
    unmasked: Contains images that could not be masked due to unreadability.

# Important Note

This tool relies on the Google Vision API, so it is imperative to have the JSON key file for authentication. Make sure to provide the correct path to the key file for seamless operation.

# Please Note:

    The tool achieves optimal results when Aadhar card images are placed in the input folder.
    Images that Vision API cannot read are moved to the unmasked folder.
    Ensure you have the required permissions and adhere to legal and ethical considerations when using this tool.

Feel free to contribute, report issues, or suggest improvements to make this Aadhar masking tool even more effective.


