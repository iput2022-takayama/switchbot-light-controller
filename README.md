# SwitchBot Light Controller

This repository contains Python scripts for managing and controlling SwitchBot devices, especially smart lights, using the SwitchBot API.

## Features
- Control SwitchBot devices (e.g., smart lights) via API
- Turn devices on/off
- Adjust brightness and color (for compatible devices)
- Retrieve device status
- Easy-to-use Python scripts for home automation

## Requirements
To use these scripts, you will need:
- Python 3.7 or higher
- A SwitchBot account
- SwitchBot API token and secret
- Installed Python libraries: `requests`, `python-dotenv`

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root of the project and add your SwitchBot API credentials:
   ```
   SWITCHBOT_TOKEN=your_switchbot_token
   SWITCHBOT_SECRET=your_switchbot_secret
   ```

4. Run the script to retrieve your device list:
   ```bash
   python get_device_list.py
   ```

5. Copy the device ID of the light you want to control and add it to your `.env` file:
   ```
   SWITCHBOT_DEVICE_ID_COLOR_BULB=your_device_id
   ```

## Usage

You can use the provided scripts to control your devices. For example:
- To turn a light on or off
- To adjust brightness or color (if supported by your device)

Example command:
```bash
python control_light.py --on
```

## File Structure
```
├── get_device_list.py    # Script to retrieve and display your SwitchBot devices
├── control_light.py      # Script to control your smart lights
├── .env                  # Environment variables (not included in the repository)
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## Notes
- Make sure to keep your `.env` file secure and do not share it publicly.
- If you encounter issues with the scripts, check your API credentials and ensure your device is online.

## License
This project is licensed under the MIT License. Feel free to use and modify it for your personal projects.

## References
- [SwitchBot API Documentation](https://github.com/OpenWonderLabs/SwitchBotAPI)
- [Python Requests Library](https://docs.python-requests.org/en/latest/)
