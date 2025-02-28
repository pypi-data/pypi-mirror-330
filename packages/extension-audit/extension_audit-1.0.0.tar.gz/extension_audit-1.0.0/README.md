# Project Overview #
This is a package for reporting and analysing data sent to the servers of chrome extensions using the MITM Proxy.

---

## Prerequisites

- A compatible operating system (Windows, macOS, Linux)
- Google Chrome browser installed
- Access to a terminal/command prompt

## Installation
1. **Download Mitmproxy**

   - Visit the [official Mitmproxy website](https://mitmproxy.org/) and follow the installation guidelines for your operating system.

2. **Install Mitmproxy Certificate**

   - Start Mitmproxy or Mitmweb by running the `mitmweb` command in the terminal.
   - Create a new Chrome profile:
     - Open Chrome.
     - At the top-right, click on the Profile icon (a circle with your account picture) and select Add.
     - In the pop-up window, choose **Continue without an account**.
     - Enter a name.
     - Click **Done**.
     - For more detailed instructions, refer to the [official Chrome help page](https://support.google.com/chrome/answer/2364824?hl=en).
     - Open Chrome and navigate to `chrome://version/`.
     - Take note of the `Executable Path` and `Profile Path`. These paths may be useful for setting up the proxy.

3. **Configure Chrome with Mitmproxy**
    ***MacOS***
    - Run the following command to start Chrome with the Mitmproxy proxy:
        ```
        open -a "Google Chrome" --args --proxy-server="http://localhost:8080"
        ```

    - If this doesn’t work, try:
        ```
        /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --proxy-server="http://localhost:8080"
        ```

    ***Windows***
   - Open the terminal and navigate to the Chrome executable. For Windows 11, the typical path is:
     ```
     C:\Program Files\Google\Chrome\Application\chrome.exe
     ```
   - Run the following command to start Chrome with the Mitmproxy proxy server:
     ```
     .\chrome.exe --proxy-server="localhost:8080" --user-data-dir="C:\Users\<YourUsername>\AppData\Local\Google\Chrome\User Data\Profile<ProfileNumber>"
     ```
     Replace `<YourUsername>` and `<ProfileNumber>` with appropriate values.

4. **Download and Install the Certificate**

   - Visit `mitm.it` in the Chrome instance configured above.
   - Download the Mitmproxy certificate.
   - Install the certificate by:
     - Navigating to Chrome's settings: `Settings → Privacy and Security → Security`.
     - Selecting **Manage Certificates** and importing the downloaded certificate into the **Trusted Root Certification Authorities**.
   - Follow the prompts to complete the installation.

5. **Verify Certificate Installation**

   - Open Chrome and navigate to:
     ```
     Settings → Privacy and Security → Security → Manage Certificates.
     ```
   - Under **Trusted Root Certification Authorities**, confirm the Mitmproxy certificate is listed.

6. **Install the extension_audit package**

    - pip install the package
    ```
    pip install extension_audit
    ```

---

# Usage #

 - run the program by specifying the extension name to be used
    ```
    extension_audit <extention_name>
    ```
    For example:
    ```
    extension_audit maxai
    ```

---

# License #
This project is licensed under the AGPL-3.0 License. See the LICENSE file for details.