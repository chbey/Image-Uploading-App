# Web Application: Image Gallery App

This web application is built using Django, HTML, and CSS. It provides a platform for users to sign up, log in, upload images with specific types, and view their uploaded images in a gallery.

## Features

1. **Signup and Login:**
   - Users can create an account by signing up with a username, email, and password.
   - Existing users can log in to their accounts.

2. **Image Upload:**
   - After login, users are redirected to the image uploading page.
   - They can choose between Portrait and Landscape image types from a select box.
   - Only JPG, GIF, or PNG image types are allowed for upload.

3. **Image Gallery:**
   - After successful image upload, users are redirected to the image gallery page.
   - The gallery displays all uploaded images in a chronological order.
   - Portrait images are displayed first, followed by Landscape images.
  
## Image Sorting Order

The image gallery is designed to display images in a specific order based on their types. Here is how the sorting works:

### Portrait Image Type

- If the first uploaded image is of the **Portrait** type, subsequent uploads of the **Portrait** type will be displayed first in the gallery.
- Following the first **Portrait** image, other image types, such as **Landscape**, will be displayed.

**Example:**
1. Portrait Image Type
2. Portrait Image Type
3. Landscape Image Type
4. Portrait Image Type
5. Landscape Image Type

### Landscape Image Type

- If the first uploaded image is of the **Landscape** type, subsequent uploads of the **Landscape** type will be displayed first in the gallery.
- Following the first **Landscape** image, other image types, such as **Portrait**, will be displayed.

**Example:**
1. Landscape Image Type
2. Portrait Image Type
3. Landscape Image Type
4. Portrait Image Type
5. Portrait Image Type

This sorting mechanism allows for a visually appealing arrangement of images in the gallery, with similar types grouped together.


## Technology Stack

- Django: A high-level Python web framework.
- HTML: Markup language for creating web pages.
- CSS: Stylesheet language for designing the web interface.

## Getting Started

### Prerequisites

- Python: Install [Python](https://www.python.org/downloads/) on your machine.

### Installation

1. Clone the repository:


### Usage

1. Sign up for a new account or log in with existing credentials.
2. After login, you will be redirected to the image upload page.
3. Choose the image type and upload an image (JPG, GIF, or PNG).
4. After a successful upload, navigate to the image gallery to view your uploaded images.
