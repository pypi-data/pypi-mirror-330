# clipboard-text-correction

Program that improves text writing.

## 1. Dependencies

This program requires **Meld** to be installed on your system to function correctly. **Meld** is a graphical tool for comparing files and directories.

How to install **Meld**:

- **Ubuntu/Debian**:

```bash
sudo apt-get install meld
```
- **Windows**: You can download the Meld installer at [http://meldmerge.org](http://meldmerge.org).


## 2. Installing

### 2.1. Install the package with pip

To install the package from `PyPI`, follow the instructions below:


```bash
pip install clipboard-text-correction
```

Execute `which clipboard-text-correction` to see where it was installed, probably in `/home/USERNAME/.local/bin/clipboard-text-correction`.

#### Using

If the program was not added to the Linux start session, then to start, use the command below:

```bash
clipboard-text-correction-indicator
```


### 2.2. Install from PYPI and add to Linux start session
Install `clipboard-text-correction` from `pypi` and add the program to the bar indicator on Linux startup session.

```bash
curl -fsSL https://raw.githubusercontent.com/trucomanx/ClipboardTextCorrection/main/install_linux_indicator_session.sh | sh
```

## 3. LLM
The program needs an API_KEY to be used. This can be obtained from
https://deepinfra.com/dash/api_keys

Place the obtained API_KEY in the program menu under `Open config file`.

## 4. Buy me a coffee

If you find this tool useful and would like to support its development, you can buy me a coffee!  
Your donations help keep the project running and improve future updates.  

[☕ Buy me a coffee](https://ko-fi.com/trucomanx) 

## 5. License

This project is licensed under the GPL license. See the `LICENSE` file for more details.
