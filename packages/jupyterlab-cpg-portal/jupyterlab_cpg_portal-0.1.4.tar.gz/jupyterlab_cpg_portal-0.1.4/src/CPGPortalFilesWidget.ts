import { JupyterFrontEnd } from '@jupyterlab/application';
import { Widget, PanelLayout } from '@lumino/widgets';
import { refreshIcon, launchIcon } from '@jupyterlab/ui-components';
// import { addJupyterLabThemeChangeListener } from '@jupyter-notebook/web-components';
import { CPGPortalDrive } from './contents';
import { ICPGPortalFile } from './cpgportal';

/**
 * Widget for browsing files using a Contents.IDrive implementation.
 */
export class CPGPortalFilesWidget extends Widget {
  private _app: JupyterFrontEnd;
  private _drive: CPGPortalDrive;
  private _fileListContainer: Widget;

  /**
   * Construct a new widget.
   *
   * @param app - JupyterFrontEnd application.
   * @param drive - A drive that implements Contents.IDrive.
   */
  constructor(app: JupyterFrontEnd, drive: CPGPortalDrive) {
    super();
    this._app = app;
    this._drive = drive;
    this.id = 'cpg-portal-files-panel';
    this.title.closable = true;
    this.addClass('cpgPortalFilesWidget');

    // Use a PanelLayout to stack the header and file list.
    const layout = new PanelLayout();
    this.layout = layout;

    // Create a flex container to replace the deprecated toolbar.
    const headerContainer = new Widget();
    headerContainer.node.style.width = '100%';
    headerContainer.node.style.display = 'flex';
    headerContainer.node.style.justifyContent = 'space-between';
    headerContainer.node.style.alignItems = 'center';
    headerContainer.node.style.padding = '0px 4px';

    // Create a title element.
    const titleElement = document.createElement('div');
    titleElement.textContent = 'CPG Portal Files';
    titleElement.classList.add('cpg-portal-title');
    headerContainer.node.appendChild(titleElement);

    // Create a container for the buttons (aligned to the right).
    const buttonContainer = document.createElement('div');
    buttonContainer.style.display = 'flex';

    // Create the refresh button using jp-button.
    const refreshBtn = document.createElement('jp-button');
    refreshBtn.setAttribute('appearance', 'stealth');
    refreshBtn.setAttribute('scale', 'medium');
    refreshBtn.setAttribute('title', 'Refresh File List');
    refreshBtn.innerHTML = refreshIcon.svgstr;
    refreshBtn.addEventListener('click', async () => {
      refreshBtn.setAttribute('disabled', 'true');
      await this.fetchFiles();
      refreshBtn.removeAttribute('disabled');
    });
    buttonContainer.appendChild(refreshBtn);

    // Create the link button using jp-button.
    const linkBtn = document.createElement('jp-button');
    linkBtn.setAttribute('appearance', 'stealth');
    linkBtn.setAttribute('scale', 'medium');
    linkBtn.setAttribute('title', 'Link to CPG Portal');
    linkBtn.innerHTML = launchIcon.svgstr;
    linkBtn.addEventListener('click', async () => {
      window.open('https://portal.cpg.unimelb.edu.au/files', '_blank');
    });
    buttonContainer.appendChild(linkBtn);

    headerContainer.node.appendChild(buttonContainer);
    layout.addWidget(headerContainer);

    // add a description
    const description = new Widget();
    description.node.textContent =
      'Browse files on the CPG Portal. Use the download button to save files to your Secure Analysis Environment.';
    description.node.style.paddingLeft = '4px';
    description.node.style.paddingRight = '4px';
    description.node.style.paddingBottom = '8px';
    description.node.style.fontSize = '0.8em';
    description.node.style.color = 'var(--jp-ui-font-color2)';
    description.node.style.borderBottom = '1px solid #ddd';
    layout.addWidget(description);

    // Create the container that will hold the file list.
    this._fileListContainer = new Widget();
    this._fileListContainer.node.style.overflowY = 'auto';
    this._fileListContainer.node.style.overflowX = 'hidden';
    this._fileListContainer.node.style.padding = '4px';
    this._fileListContainer.node.style.paddingTop = '0px';
    // Set a max-height to prevent the file list from taking up the entire panel.
    this._fileListContainer.node.style.maxHeight = 'calc(100vh - 100px)';
    layout.addWidget(this._fileListContainer);

    // Listen for theme changes.
    // addJupyterLabThemeChangeListener();
  }

  /**
   * Fetch the list of files from the drive.
   */
  public async fetchFiles(): Promise<void> {
    this._clearFileList();
    try {
      // Fetch the root directory. Change '' to another path if needed.
      const model = await this._drive.get('', { content: true });
      if (
        !model.content ||
        (Array.isArray(model.content) && model.content.length === 0)
      ) {
        this._showMessage('No files found.');
        return;
      }
      // Add a header row.
      this._addFileListHeader();
      // Iterate over the directory contents.
      for (const file of model.content as ICPGPortalFile[]) {
        this._addFileRow(file);
      }
    } catch (error) {
      this._showError(`Error fetching files: ${String(error)}`);
      console.error('Error fetching files:', error);
    }
  }

  /**
   * Clear all content from the file list container.
   */
  private _clearFileList(): void {
    while (this._fileListContainer.node.firstChild) {
      this._fileListContainer.node.removeChild(
        this._fileListContainer.node.firstChild
      );
    }
  }

  /**
   * Display an error message.
   */
  private _showError(message: string): void {
    const errorWidget = new Widget();
    errorWidget.node.textContent = message;
    errorWidget.addClass('cpg-portal-error');
    this._fileListContainer.node.appendChild(errorWidget.node);
  }

  /**
   * Display a simple informational message.
   */
  private _showMessage(message: string): void {
    const msgWidget = new Widget();
    msgWidget.node.textContent = message;
    msgWidget.addClass('cpg-portal-message');
    this._fileListContainer.node.appendChild(msgWidget.node);
  }

  /**
   * Add a header row to the file list.
   */
  private _addFileListHeader(): void {
    const header = new Widget();
    header.node.style.display = 'flex';
    header.node.style.fontWeight = 'bold';
    header.node.style.paddingLeft = '4px';
    header.node.style.paddingBottom = '4px';
    header.node.style.paddingTop = '4px';
    header.node.style.borderBottom = '1px solid #ddd';
    header.node.style.position = 'sticky';
    header.node.style.top = '0';
    header.node.style.zIndex = '1';
    header.node.style.backgroundColor = 'var(--jp-layout-color1)';
    header.node.style.color = 'var(--jp-ui-font-color1)';
    header.node.style.fontSize = 'var(--jp-ui-font-size1)';

    const nameCol = new Widget();
    nameCol.node.textContent = 'File Name';
    nameCol.node.style.flex = '4';

    const createdCol = new Widget();
    createdCol.node.textContent = 'Created';
    createdCol.node.style.flex = '2';
    createdCol.node.style.textAlign = 'right';

    const sizeCol = new Widget();
    sizeCol.node.textContent = 'Size';
    sizeCol.node.style.flex = '2';
    sizeCol.node.style.textAlign = 'right';

    const actionCol = new Widget();
    actionCol.node.style.flex = '1';
    actionCol.node.style.textAlign = 'right';
    actionCol.node.style.width = '25px';

    header.node.appendChild(nameCol.node);
    header.node.appendChild(createdCol.node);
    header.node.appendChild(sizeCol.node);
    header.node.appendChild(actionCol.node);

    this._fileListContainer.node.appendChild(header.node);
  }

  /**
   * Add a row widget for an individual file.
   *
   * @param file - A Contents.IModel representing a file or directory.
   */
  private _addFileRow(file: ICPGPortalFile): void {
    const row = new Widget();
    row.node.style.display = 'flex';
    row.node.style.alignItems = 'center';
    row.node.style.paddingLeft = '4px';

    // File name column.
    const nameWidget = new Widget();
    nameWidget.node.textContent = file.name;
    nameWidget.node.style.flex = '4';
    nameWidget.node.style.whiteSpace = 'nowrap';
    nameWidget.node.style.overflow = 'hidden';
    nameWidget.node.style.textOverflow = 'ellipsis';

    // Created date column.
    const createdWidget = new Widget();
    const created = file.created_at
      ? this._timeSince(new Date(file.created_at))
      : '';
    createdWidget.node.textContent = created;
    createdWidget.node.style.flex = '2';
    createdWidget.node.style.textAlign = 'right';
    createdWidget.node.style.whiteSpace = 'nowrap';

    // Size column (if available).
    const sizeWidget = new Widget();
    const size = (file as any).size
      ? this._formatBytes((file as any).size, 0)
      : '';
    sizeWidget.node.textContent = size;
    sizeWidget.node.style.flex = '2';
    sizeWidget.node.style.textAlign = 'right';
    sizeWidget.node.style.whiteSpace = 'nowrap';

    // Action column (download button for files).
    const actionWidget = new Widget();
    actionWidget.node.style.flex = '1';
    actionWidget.node.style.textAlign = 'right';
    actionWidget.node.style.width = '25px';

    const designSystemProvider = document.createElement(
      'jp-design-system-provider'
    );
    designSystemProvider.style.width = 'auto';

    const downloadBtn = document.createElement('jp-button');
    downloadBtn.setAttribute('appearance', 'stealth');
    downloadBtn.setAttribute('scale', 'medium');
    downloadBtn.classList.add('download-btn');
    downloadBtn.setAttribute('title', 'Download File');
    downloadBtn.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
      </svg>
    `;
    downloadBtn.addEventListener('click', async () => {
      downloadBtn.setAttribute('disabled', 'true');
      const originalContent = downloadBtn.innerHTML;
      downloadBtn.innerHTML =
        '<jp-progress-ring style="height: 17px;"></jp-progress-ring>';
      await this.downloadFile(file);
      downloadBtn.removeAttribute('disabled');
      downloadBtn.innerHTML = originalContent;
    });

    designSystemProvider.appendChild(downloadBtn);
    actionWidget.node.appendChild(designSystemProvider);

    row.node.appendChild(nameWidget.node);
    row.node.appendChild(createdWidget.node);
    row.node.appendChild(sizeWidget.node);
    row.node.appendChild(actionWidget.node);

    this._fileListContainer.node.appendChild(row.node);
  }

  /**
   * Format bytes into a human-readable string.
   */
  private _formatBytes(bytes: number, decimals = 2): string {
    if (bytes === 0) {
      return '0 B';
    }
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
  }

  /**
   * Calculate the time elapsed since a given date.
   * @param date - The date to calculate from.
   * @returns A string representing the elapsed time.
   */
  private _timeSince(date: Date): string {
    const seconds = Math.floor((new Date().getTime() - date.getTime()) / 1000);
    let interval = Math.floor(seconds / 31536000);
    if (interval >= 1) {
      return interval + 'Y' + ' ago';
    }
    interval = Math.floor(seconds / 2592000);
    if (interval >= 1) {
      return interval + 'M' + ' ago';
    }
    interval = Math.floor(seconds / 86400);
    if (interval >= 1) {
      return interval + 'd' + ' ago';
    }
    interval = Math.floor(seconds / 3600);
    if (interval >= 1) {
      return interval + 'h' + ' ago';
    }
    interval = Math.floor(seconds / 60);
    if (interval >= 1) {
      return interval + 'm' + ' ago';
    }
    return Math.floor(seconds) + 's' + ' ago';
  }

  /**
   * Download a file using the drive's getDownloadUrl method.
   * @param file - The Contents.IModel representing the file.
   */
  private async downloadFile(file: ICPGPortalFile): Promise<void> {
    try {
      const url = await this._drive.getDownloadUrl(file.id);
      const response = await fetch(url, {
        headers: {
          Authorization: `Bearer ${this._drive.accessToken}`
        }
      });
      if (!response.ok) {
        return;
      }
      const blob = await response.blob();
      // Save file based on MIME type.
      if (blob.type.startsWith('text/')) {
        const textContent = await blob.text();
        await this._app.serviceManager.contents.save(file.name, {
          type: 'file',
          format: 'text',
          content: textContent
        });
      } else {
        const reader = new FileReader();
        reader.onload = async event => {
          const dataUrl = event.target?.result;
          if (typeof dataUrl === 'string') {
            const base64Data = dataUrl.split(',')[1];
            try {
              await this._app.serviceManager.contents.save(file.name, {
                type: 'file',
                format: 'base64',
                content: base64Data
              });
            } catch (error) {
              console.error('Error saving file:', error);
            }
          }
        };
        reader.readAsDataURL(blob);
      }
    } catch (error) {
      console.error(`Error downloading file ${file.name}:`, error);
    }
  }
}
