# Random Color Add-on for Blender

A Blender add-on that assigns random colors to selected faces with auto-update capabilities.

## Features

- 🎨 **Random Color Assignment**: Assign random colors to selected faces
- 🧹 **Clear Colors**: Remove random colors from selected faces  
- 🗿 **FaceSet Creation**: Create FaceSets for sculpting workflow
- 🧰 **Material Management**: Clean up unused materials
- 🔄 **Auto-Update**: Automatic updates from GitHub releases
- 🔧 **Development Tools**: Reload add-on without restarting Blender

## Installation

### For Users
1. Download the latest release from [GitHub Releases](https://github.com/triemnguyen123/RandomColor/releases)
2. In Blender: Edit > Preferences > Add-ons > Install
3. Select the downloaded `.zip` file
4. Enable "Random Color" add-on

### For Developers
```bash
# Clone the repository
git clone https://github.com/triemnguyen123/RandomColor.git
cd RandomColor

# Setup development environment
python scripts/dev_setup.py

# For symlink development (Linux/macOS)
python scripts/dev_setup.py symlink
```

## Usage

1. **Select faces** in Edit mode
2. **Open the Random Color panel** in the 3D Viewport sidebar
3. **Click "Random Color Selected Faces"** to assign random colors
4. **Use "Clear Random Color Selected Faces"** to remove colors

### Additional Features

- **FaceSet for Sculpting**: Create FaceSets from selected faces
- **Material Cleanup**: Remove unused RandomSel materials
- **Auto-Update**: Check for updates and install automatically
- **Development Reload**: Reload add-on during development

## Development

### Project Structure
```
random_color_addon/
├── __init__.py              # Main add-on file
├── core/
│   ├── __init__.py
│   ├── operators.py         # Core operators
│   ├── ui.py               # UI components
│   ├── materials.py        # Material management
│   └── updater.py          # Auto-update system
└── scripts/
    ├── dev_setup.py        # Development setup
    └── create_release.py   # Release creation
```

### Creating a Release

1. **Update version** in `random_color_addon/__init__.py`
2. **Run release script**:
   ```bash
   python scripts/create_release.py 1.0.1
   ```
3. **GitHub Actions** will automatically:
   - Build the release package
   - Create GitHub release
   - Upload the add-on file

### Development Workflow

1. **Make changes** to the code
2. **Use "Reload Add-on"** button in Blender (no restart needed!)
3. **Test** your changes
4. **Commit** and push to GitHub
5. **Create release** when ready

## Auto-Update System

The add-on includes an automatic update system:

- **Check for Updates**: Manually check for new versions
- **Auto-Install**: Automatically download and install updates
- **Version Display**: Shows current version in the UI

### Setup for Auto-Update

1. **Create GitHub repository** with the same name
2. **Update repository URL** in `random_color_addon/core/updater.py`
3. **Create releases** with version tags (e.g., `v1.0.1`)

## Requirements

- Blender 3.0+
- Python 3.7+ (for development)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

- **Issues**: [GitHub Issues](https://github.com/triemnguyen123/RandomColor/issues)
- **Documentation**: [GitHub Wiki](https://github.com/triemnguyen123/RandomColor/wiki)

## Changelog

### v1.0.0
- Initial release
- Random color assignment to selected faces
- Material management utilities
- Auto-update system
- Development tools
### v1.0.1
- Add Macro Faceset From visible
- 
