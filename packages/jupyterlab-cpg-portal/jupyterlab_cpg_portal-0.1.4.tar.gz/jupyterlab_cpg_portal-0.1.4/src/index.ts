// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

import {
  ILayoutRestorer,
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { ICommandPalette, WidgetTracker } from '@jupyterlab/apputils';

import { LabIcon } from '@jupyterlab/ui-components';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import { CPGPortalDrive, DEFAULT_CPG_PORTAL_BASE_URL } from './contents';

import { CPGPortalFilesWidget } from './CPGPortalFilesWidget';

/**
 * GitLab filebrowser plugin state namespace.
 */
const NAMESPACE = 'jupyterlab_cpg_portal';
/**
 * The ID for the plugin.
 */
const PLUGIN_ID = `${NAMESPACE}:plugin`;
const COMMAND_ID = `${NAMESPACE}:open`;
/**
 * GitLab Icon class.
 */
export const cpgLabIcon = new LabIcon({
  name: `${NAMESPACE}:icon`,
  svgstr: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0.872 0.137 505.152 505.152" width="500px" height="500px">
    <path fill="#616161" class="jp-icon3 jp-icon-selectable" d="M 506.024 252.713 C 506.024 392.207 392.942 505.289 253.448 505.289 C 113.954 505.289 0.872 392.207 0.872 252.713 C 0.872 113.219 113.954 0.137 253.448 0.137 C 392.942 0.137 506.024 113.219 506.024 252.713 Z M 186.982 369.339 C 193.183 373.48 199.997 372.091 207.298 365.898 C 213.97 360.237 221.452 357.069 230.408 357.256 C 241.725 357.492 253.092 357.873 264.364 357.107 C 280.136 356.036 294.673 358.319 307.212 368.674 C 307.839 369.192 308.623 369.814 309.363 369.854 C 313.68 370.09 318.395 371.331 322.243 370.043 C 329.215 367.708 331.892 361.413 332.29 354.328 C 332.748 346.173 330.422 339.048 322.977 334.826 C 316.421 331.108 310.296 333.967 305.164 338.035 C 296.45 344.942 286.817 348.051 275.759 347.77 C 264.61 347.487 253.428 347.302 242.296 347.83 C 227.901 348.514 214.983 345.817 203.316 336.555 C 194.474 329.537 184.494 332.992 180.161 343.547 C 177.744 349.436 177.884 355.487 180.294 361.795 C 182.635 364.564 184.376 367.599 186.982 369.339 Z M 307.553 413.442 C 308.65 410.086 309.262 406.466 309.433 402.934 C 309.808 395.205 306.952 388.805 299.613 385.587 C 292.503 382.47 286.315 384.718 280.55 389.763 C 274.07 395.434 266.062 397.802 257.536 398.525 C 246.551 399.455 237.448 394.946 228.62 389.112 C 225.428 387.003 221.615 384.865 217.961 384.622 C 209.905 384.087 202.896 389.406 201.789 397.021 C 200.106 408.61 201.215 415.556 209.631 420.665 C 215.962 424.509 222.964 423.433 230.391 417.29 C 237.895 411.082 246.68 407.864 256.075 407.96 C 267.191 408.074 276.82 413.072 285.44 420.633 C 294.506 425.486 304.877 421.625 307.553 413.442 Z M 308.743 307.256 C 310.933 299.011 307.857 289.148 301.535 284.858 C 295.981 281.09 289.754 281.971 281.846 287.638 C 281.035 288.219 280.219 288.795 279.388 289.347 C 268.755 296.404 257.124 299.453 244.821 295.541 C 238.477 293.524 232.594 289.694 226.905 286.054 C 216.852 279.623 211.346 280.782 204.59 290.187 C 202.428 293.196 201.486 297.606 201.342 301.426 C 201.061 308.828 204.011 315.238 210.702 318.968 C 217.223 322.602 223.086 320.09 228.589 315.96 C 231.868 313.499 235.137 310.673 238.881 309.244 C 256.344 302.577 272.035 306.045 286.136 318.703 C 296.887 324.302 306.099 317.206 308.743 307.256 Z M 282.369 84.005 C 268.181 96.065 245.611 96.6 231.902 85.935 C 228.283 83.12 223.982 81.055 219.744 79.223 C 217.877 78.416 215.129 78.392 213.225 79.142 C 204.584 82.545 200.579 90.582 201.902 101.18 C 202.754 108.001 206.212 113.093 212.731 115.521 C 218.674 117.734 223.656 115.515 228.317 111.588 C 231.047 109.286 234.151 106.998 237.481 105.909 C 254.322 100.402 270.291 100.448 284.613 113.176 C 290.798 118.673 298.54 117.396 304.191 111.359 C 313.85 101.041 308.734 82.718 294.722 78.931 C 290.282 80.565 285.515 81.331 282.369 84.005 Z M 203.052 192.407 C 199.658 200.575 202.148 210.446 208.721 215.452 C 214.874 220.14 221.238 219.337 229.464 212.836 C 245.039 200.527 266.514 200.89 282.883 213.74 C 293.681 222.217 305.265 218.22 308.641 204.853 C 310.718 196.627 307.512 187.235 301.197 183.051 C 295.371 179.19 289.89 180.056 281.764 186.122 C 281.231 186.52 280.721 186.951 280.171 187.323 C 266.352 196.675 252.04 198.463 237.103 190.055 C 233.632 188.102 230.182 186.103 226.806 183.992 C 219.004 179.113 213.411 179.705 206.476 186.517 C 205.162 188.658 203.871 190.435 203.052 192.407 Z M 248.733 429.27 C 240.563 431.96 235.793 442.375 240.423 453.072 C 243.231 459.561 255.123 463.109 262.432 459.85 C 270.222 456.376 273.308 449.618 271.64 439.68 C 270.582 433.38 264.051 428.555 255.901 428.379 C 253.211 428.655 250.844 428.574 248.733 429.27 Z M 244.587 238.718 C 239.495 243.61 238.371 249.566 240.553 256.069 C 242.78 262.707 248.357 266.319 255.46 266.199 C 263 266.072 268.105 262.546 270.271 255.969 C 272.736 248.486 270.703 242.217 263.831 236.968 C 255.895 233.368 249.512 233.988 244.587 238.718 Z M 266.078 74.647 C 271.286 69.852 272.628 61.199 269.171 54.978 C 265.778 48.875 258.105 45.732 251.172 47.607 C 244.002 49.546 239.606 55.504 239.723 63.126 C 239.905 75.061 250.167 81.082 263.336 76.585 C 264.463 75.802 265.353 75.314 266.078 74.647 Z M 184.728 163.897 C 190.93 168.038 197.744 166.649 205.044 160.455 C 211.716 154.795 219.199 151.627 228.154 151.813 C 239.472 152.049 250.839 152.431 262.111 151.665 C 277.882 150.593 292.419 152.877 304.958 163.231 C 305.586 163.749 306.369 164.371 307.109 164.412 C 311.426 164.648 316.141 165.888 319.989 164.6 C 326.962 162.266 329.639 155.97 330.037 148.886 C 330.494 140.731 328.168 133.605 320.723 129.383 C 314.167 125.666 308.043 128.525 302.911 132.592 C 294.196 139.5 284.563 142.608 273.505 142.327 C 262.356 142.044 251.174 141.859 240.043 142.388 C 225.647 143.071 212.73 140.374 201.063 131.113 C 192.221 124.094 182.241 127.55 177.908 138.105 C 175.49 143.994 175.631 150.045 178.041 156.352 C 180.382 159.121 182.123 162.157 184.728 163.897 Z"   />
  </svg>`
});

/**
 * The JupyterLab plugin for the GitLab Filebrowser.
 */
const fileBrowserPlugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  requires: [ICommandPalette],
  optional: [ILayoutRestorer, ISettingRegistry],
  activate: activateFileBrowser,
  autoStart: true
};

/**
 * Activate the file browser.
 */
function activateFileBrowser(
  app: JupyterFrontEnd,
  palette: ICommandPalette,
  restorer: ILayoutRestorer,
  settingRegistry: ISettingRegistry
): void {
  let widget: CPGPortalFilesWidget | null = null;

  app.commands.addCommand(COMMAND_ID, {
    label: 'Open CPG Portal Files',
    execute: async () => {
      const drive = new CPGPortalDrive(app.docRegistry);

      if (settingRegistry) {
        const settings = await settingRegistry.load(PLUGIN_ID);
        console.log(settings);
        const baseUrl = settings.get('portalUrl').composite as
          | string
          | null
          | undefined;
        const accessToken = settings.get('apiToken').composite as
          | string
          | null
          | undefined;
        drive.baseUrl = baseUrl || DEFAULT_CPG_PORTAL_BASE_URL;
        drive.accessToken =
          accessToken || window.localStorage.getItem('access_token');
      }
      // Create the widget if it doesn't exist.
      if (!widget || widget.isDisposed) {
        widget = new CPGPortalFilesWidget(app, drive);
        widget.title.icon = cpgLabIcon;
        widget.title.iconClass = 'jp-SideBar-tabIcon';
        widget.title.caption = 'Browse CPG Portal';
        //widget.id = 'cpg-portal-file-browser';
      }
      if (!widget.isAttached) {
        app.shell.add(widget, 'left', { rank: 102 });
      }
      await widget.fetchFiles();
      app.shell.activateById(widget.id);
    }
  });
  
  // palette.addItem({ command: COMMAND_ID, category: 'CPG Portal' });

  const tracker = new WidgetTracker<CPGPortalFilesWidget>({
    namespace: NAMESPACE
  });
  if (restorer) {
    restorer.restore(tracker, {
      command: COMMAND_ID,
      name: () => NAMESPACE
    });
  }

  // Automatically open the panel on startup.
  app.commands.execute(COMMAND_ID);
  return;
}

export default fileBrowserPlugin;