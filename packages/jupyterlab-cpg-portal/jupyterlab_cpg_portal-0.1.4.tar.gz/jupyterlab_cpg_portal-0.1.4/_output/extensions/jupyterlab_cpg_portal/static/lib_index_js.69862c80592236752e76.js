"use strict";
(self["webpackChunkjupyterlab_cpg_portal"] = self["webpackChunkjupyterlab_cpg_portal"] || []).push([["lib_index_js"],{

/***/ "./lib/CPGPortalFilesWidget.js":
/*!*************************************!*\
  !*** ./lib/CPGPortalFilesWidget.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CPGPortalFilesWidget: () => (/* binding */ CPGPortalFilesWidget)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Widget for browsing files using a Contents.IDrive implementation.
 */
class CPGPortalFilesWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    /**
     * Construct a new widget.
     *
     * @param app - JupyterFrontEnd application.
     * @param drive - A drive that implements Contents.IDrive.
     */
    constructor(app, drive) {
        super();
        this._app = app;
        this._drive = drive;
        this.id = 'cpg-portal-files-panel';
        this.title.closable = true;
        this.addClass('cpgPortalFilesWidget');
        // Use a PanelLayout to stack the header and file list.
        const layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.PanelLayout();
        this.layout = layout;
        // Create a flex container to replace the deprecated toolbar.
        const headerContainer = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
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
        refreshBtn.innerHTML = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.refreshIcon.svgstr;
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
        linkBtn.innerHTML = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.launchIcon.svgstr;
        linkBtn.addEventListener('click', async () => {
            window.open('https://portal.cpg.unimelb.edu.au/files', '_blank');
        });
        buttonContainer.appendChild(linkBtn);
        headerContainer.node.appendChild(buttonContainer);
        layout.addWidget(headerContainer);
        // add a description
        const description = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
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
        this._fileListContainer = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
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
    async fetchFiles() {
        this._clearFileList();
        try {
            // Fetch the root directory. Change '' to another path if needed.
            const model = await this._drive.get('', { content: true });
            if (!model.content ||
                (Array.isArray(model.content) && model.content.length === 0)) {
                this._showMessage('No files found.');
                return;
            }
            // Add a header row.
            this._addFileListHeader();
            // Iterate over the directory contents.
            for (const file of model.content) {
                this._addFileRow(file);
            }
        }
        catch (error) {
            this._showError(`Error fetching files: ${String(error)}`);
            console.error('Error fetching files:', error);
        }
    }
    /**
     * Clear all content from the file list container.
     */
    _clearFileList() {
        while (this._fileListContainer.node.firstChild) {
            this._fileListContainer.node.removeChild(this._fileListContainer.node.firstChild);
        }
    }
    /**
     * Display an error message.
     */
    _showError(message) {
        const errorWidget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
        errorWidget.node.textContent = message;
        errorWidget.addClass('cpg-portal-error');
        this._fileListContainer.node.appendChild(errorWidget.node);
    }
    /**
     * Display a simple informational message.
     */
    _showMessage(message) {
        const msgWidget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
        msgWidget.node.textContent = message;
        msgWidget.addClass('cpg-portal-message');
        this._fileListContainer.node.appendChild(msgWidget.node);
    }
    /**
     * Add a header row to the file list.
     */
    _addFileListHeader() {
        const header = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
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
        const nameCol = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
        nameCol.node.textContent = 'File Name';
        nameCol.node.style.flex = '4';
        const createdCol = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
        createdCol.node.textContent = 'Created';
        createdCol.node.style.flex = '2';
        createdCol.node.style.textAlign = 'right';
        const sizeCol = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
        sizeCol.node.textContent = 'Size';
        sizeCol.node.style.flex = '2';
        sizeCol.node.style.textAlign = 'right';
        const actionCol = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
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
    _addFileRow(file) {
        const row = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
        row.node.style.display = 'flex';
        row.node.style.alignItems = 'center';
        row.node.style.paddingLeft = '4px';
        // File name column.
        const nameWidget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
        nameWidget.node.textContent = file.name;
        nameWidget.node.style.flex = '4';
        nameWidget.node.style.whiteSpace = 'nowrap';
        nameWidget.node.style.overflow = 'hidden';
        nameWidget.node.style.textOverflow = 'ellipsis';
        // Created date column.
        const createdWidget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
        const created = file.created_at
            ? this._timeSince(new Date(file.created_at))
            : '';
        createdWidget.node.textContent = created;
        createdWidget.node.style.flex = '2';
        createdWidget.node.style.textAlign = 'right';
        createdWidget.node.style.whiteSpace = 'nowrap';
        // Size column (if available).
        const sizeWidget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
        const size = file.size
            ? this._formatBytes(file.size, 0)
            : '';
        sizeWidget.node.textContent = size;
        sizeWidget.node.style.flex = '2';
        sizeWidget.node.style.textAlign = 'right';
        sizeWidget.node.style.whiteSpace = 'nowrap';
        // Action column (download button for files).
        const actionWidget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
        actionWidget.node.style.flex = '1';
        actionWidget.node.style.textAlign = 'right';
        actionWidget.node.style.width = '25px';
        const designSystemProvider = document.createElement('jp-design-system-provider');
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
    _formatBytes(bytes, decimals = 2) {
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
    _timeSince(date) {
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
    async downloadFile(file) {
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
            }
            else {
                const reader = new FileReader();
                reader.onload = async (event) => {
                    var _a;
                    const dataUrl = (_a = event.target) === null || _a === void 0 ? void 0 : _a.result;
                    if (typeof dataUrl === 'string') {
                        const base64Data = dataUrl.split(',')[1];
                        try {
                            await this._app.serviceManager.contents.save(file.name, {
                                type: 'file',
                                format: 'base64',
                                content: base64Data
                            });
                        }
                        catch (error) {
                            console.error('Error saving file:', error);
                        }
                    }
                };
                reader.readAsDataURL(blob);
            }
        }
        catch (error) {
            console.error(`Error downloading file ${file.name}:`, error);
        }
    }
}


/***/ }),

/***/ "./lib/contents.js":
/*!*************************!*\
  !*** ./lib/contents.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CPGPortalDrive: () => (/* binding */ CPGPortalDrive),
/* harmony export */   DEFAULT_CPG_PORTAL_BASE_URL: () => (/* binding */ DEFAULT_CPG_PORTAL_BASE_URL)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/observables */ "webpack/sharing/consume/default/@jupyterlab/observables");
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_observables__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




const DEFAULT_CPG_PORTAL_BASE_URL = 'https://portal.cpg.unimelb.edu.au';
/**
 * A Contents.IDrive implementation that serves as a read-only
 * view onto GitLab repositories.
 */
class CPGPortalDrive {
    /**
     * Construct a new drive object.
     *
     * @param options - The options used to initialize the object.
     */
    constructor(registry) {
        this._baseUrl = '';
        this._validToken = false;
        this._isDisposed = false;
        this._fileChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this._serverSettings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__.ServerConnection.makeSettings();
        this.baseUrl = DEFAULT_CPG_PORTAL_BASE_URL;
        this.errorState = new _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_2__.ObservableValue(false);
    }
    /**
     * The name of the drive.
     */
    get name() {
        return 'CPG Portal';
    }
    /**
     * State for whether the user is valid.
     */
    get validToken() {
        return this._validToken;
    }
    /**
     * Settings for the notebook server.
     */
    get serverSettings() {
        return this._serverSettings;
    }
    /**
     * A signal emitted when a file operation takes place.
     */
    get fileChanged() {
        return this._fileChanged;
    }
    /**
     * Test whether the manager has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the manager.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal.clearData(this);
    }
    /**
     * The GitLab base URL
     */
    get baseUrl() {
        return this._baseUrl;
    }
    /**
     * The GitLab base URL is set by the settingsRegistry change hook
     */
    set baseUrl(url) {
        this._baseUrl = url;
    }
    /**
     * The GitLab access token
     */
    get accessToken() {
        return this._accessToken;
    }
    /**
     * The GitLab access token is set by the settingsRegistry change hook
     */
    set accessToken(token) {
        this._accessToken = token;
    }
    // Minimal implementation of 'get' to fetch a directory model.
    async get(path, options) {
        const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(this.baseUrl, 'api', 'v1', 'files');
        console.log('Fetching files from', url);
        console.log('Using access token', this.accessToken);
        const response = await fetch(url, {
            headers: {
                Authorization: `Bearer ${this.accessToken}`
            }
        });
        if (!response.ok) {
            this.errorState.set(true);
            if (response.status === 401) {
                this._validToken = false;
                throw new Error('Invalid access token');
            }
            throw new Error(`Error fetching files: ${response.statusText}`);
        }
        this._validToken = true;
        this.errorState.set(false);
        const data = await response.json();
        const files = data.data || [];
        return {
            name: '',
            path: '',
            format: 'json',
            type: 'directory',
            created: '',
            last_modified: '',
            writable: false,
            mimetype: '',
            content: files
        };
    }
    async getDownloadUrl(path) {
        return _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(this.baseUrl, 'api', 'v1', 'files', path, 'download');
    }
    /**
     * Create a new untitled file or directory in the specified directory path.
     *
     * @param options: The options used to create the file.
     *
     * @returns A promise which resolves with the created file content when the
     *    file is created.
     */
    newUntitled(options = {}) {
        return Promise.reject('Repository is read only');
    }
    /**
     * Delete a file.
     *
     * @param path - The path to the file.
     *
     * @returns A promise which resolves when the file is deleted.
     */
    delete(path) {
        return Promise.reject('Repository is read only');
    }
    /**
     * Rename a file or directory.
     *
     * @param path - The original file path.
     *
     * @param newPath - The new file path.
     *
     * @returns A promise which resolves with the new file contents model when
     *   the file is renamed.
     */
    rename(path, newPath) {
        return Promise.reject('Repository is read only');
    }
    /**
     * Save a file.
     *
     * @param path - The desired file path.
     *
     * @param options - Optional overrides to the model.
     *
     * @returns A promise which resolves with the file content model when the
     *   file is saved.
     */
    save(path, options) {
        return Promise.reject('Repository is read only');
    }
    /**
     * Copy a file into a given directory.
     *
     * @param path - The original file path.
     *
     * @param toDir - The destination directory path.
     *
     * @returns A promise which resolves with the new contents model when the
     *  file is copied.
     */
    copy(fromFile, toDir) {
        return Promise.reject('Repository is read only');
    }
    /**
     * Create a checkpoint for a file.
     *
     * @param path - The path of the file.
     *
     * @returns A promise which resolves with the new checkpoint model when the
     *   checkpoint is created.
     */
    createCheckpoint(path) {
        return Promise.reject('Repository is read only');
    }
    /**
     * List available checkpoints for a file.
     *
     * @param path - The path of the file.
     *
     * @returns A promise which resolves with a list of checkpoint models for
     *    the file.
     */
    listCheckpoints(path) {
        return Promise.resolve([]);
    }
    /**
     * Restore a file to a known checkpoint state.
     *
     * @param path - The path of the file.
     *
     * @param checkpointID - The id of the checkpoint to restore.
     *
     * @returns A promise which resolves when the checkpoint is restored.
     */
    restoreCheckpoint(path, checkpointID) {
        return Promise.reject('Repository is read only');
    }
    /**
     * Delete a checkpoint for a file.
     *
     * @param path - The path of the file.
     *
     * @param checkpointID - The id of the checkpoint to delete.
     *
     * @returns A promise which resolves when the checkpoint is deleted.
     */
    deleteCheckpoint(path, checkpointID) {
        return Promise.reject('Read only');
    }
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   cpgLabIcon: () => (/* binding */ cpgLabIcon),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _contents__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./contents */ "./lib/contents.js");
/* harmony import */ var _CPGPortalFilesWidget__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./CPGPortalFilesWidget */ "./lib/CPGPortalFilesWidget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.






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
const cpgLabIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.LabIcon({
    name: `${NAMESPACE}:icon`,
    svgstr: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0.872 0.137 505.152 505.152" width="500px" height="500px">
    <path fill="#616161" class="jp-icon3 jp-icon-selectable" d="M 506.024 252.713 C 506.024 392.207 392.942 505.289 253.448 505.289 C 113.954 505.289 0.872 392.207 0.872 252.713 C 0.872 113.219 113.954 0.137 253.448 0.137 C 392.942 0.137 506.024 113.219 506.024 252.713 Z M 186.982 369.339 C 193.183 373.48 199.997 372.091 207.298 365.898 C 213.97 360.237 221.452 357.069 230.408 357.256 C 241.725 357.492 253.092 357.873 264.364 357.107 C 280.136 356.036 294.673 358.319 307.212 368.674 C 307.839 369.192 308.623 369.814 309.363 369.854 C 313.68 370.09 318.395 371.331 322.243 370.043 C 329.215 367.708 331.892 361.413 332.29 354.328 C 332.748 346.173 330.422 339.048 322.977 334.826 C 316.421 331.108 310.296 333.967 305.164 338.035 C 296.45 344.942 286.817 348.051 275.759 347.77 C 264.61 347.487 253.428 347.302 242.296 347.83 C 227.901 348.514 214.983 345.817 203.316 336.555 C 194.474 329.537 184.494 332.992 180.161 343.547 C 177.744 349.436 177.884 355.487 180.294 361.795 C 182.635 364.564 184.376 367.599 186.982 369.339 Z M 307.553 413.442 C 308.65 410.086 309.262 406.466 309.433 402.934 C 309.808 395.205 306.952 388.805 299.613 385.587 C 292.503 382.47 286.315 384.718 280.55 389.763 C 274.07 395.434 266.062 397.802 257.536 398.525 C 246.551 399.455 237.448 394.946 228.62 389.112 C 225.428 387.003 221.615 384.865 217.961 384.622 C 209.905 384.087 202.896 389.406 201.789 397.021 C 200.106 408.61 201.215 415.556 209.631 420.665 C 215.962 424.509 222.964 423.433 230.391 417.29 C 237.895 411.082 246.68 407.864 256.075 407.96 C 267.191 408.074 276.82 413.072 285.44 420.633 C 294.506 425.486 304.877 421.625 307.553 413.442 Z M 308.743 307.256 C 310.933 299.011 307.857 289.148 301.535 284.858 C 295.981 281.09 289.754 281.971 281.846 287.638 C 281.035 288.219 280.219 288.795 279.388 289.347 C 268.755 296.404 257.124 299.453 244.821 295.541 C 238.477 293.524 232.594 289.694 226.905 286.054 C 216.852 279.623 211.346 280.782 204.59 290.187 C 202.428 293.196 201.486 297.606 201.342 301.426 C 201.061 308.828 204.011 315.238 210.702 318.968 C 217.223 322.602 223.086 320.09 228.589 315.96 C 231.868 313.499 235.137 310.673 238.881 309.244 C 256.344 302.577 272.035 306.045 286.136 318.703 C 296.887 324.302 306.099 317.206 308.743 307.256 Z M 282.369 84.005 C 268.181 96.065 245.611 96.6 231.902 85.935 C 228.283 83.12 223.982 81.055 219.744 79.223 C 217.877 78.416 215.129 78.392 213.225 79.142 C 204.584 82.545 200.579 90.582 201.902 101.18 C 202.754 108.001 206.212 113.093 212.731 115.521 C 218.674 117.734 223.656 115.515 228.317 111.588 C 231.047 109.286 234.151 106.998 237.481 105.909 C 254.322 100.402 270.291 100.448 284.613 113.176 C 290.798 118.673 298.54 117.396 304.191 111.359 C 313.85 101.041 308.734 82.718 294.722 78.931 C 290.282 80.565 285.515 81.331 282.369 84.005 Z M 203.052 192.407 C 199.658 200.575 202.148 210.446 208.721 215.452 C 214.874 220.14 221.238 219.337 229.464 212.836 C 245.039 200.527 266.514 200.89 282.883 213.74 C 293.681 222.217 305.265 218.22 308.641 204.853 C 310.718 196.627 307.512 187.235 301.197 183.051 C 295.371 179.19 289.89 180.056 281.764 186.122 C 281.231 186.52 280.721 186.951 280.171 187.323 C 266.352 196.675 252.04 198.463 237.103 190.055 C 233.632 188.102 230.182 186.103 226.806 183.992 C 219.004 179.113 213.411 179.705 206.476 186.517 C 205.162 188.658 203.871 190.435 203.052 192.407 Z M 248.733 429.27 C 240.563 431.96 235.793 442.375 240.423 453.072 C 243.231 459.561 255.123 463.109 262.432 459.85 C 270.222 456.376 273.308 449.618 271.64 439.68 C 270.582 433.38 264.051 428.555 255.901 428.379 C 253.211 428.655 250.844 428.574 248.733 429.27 Z M 244.587 238.718 C 239.495 243.61 238.371 249.566 240.553 256.069 C 242.78 262.707 248.357 266.319 255.46 266.199 C 263 266.072 268.105 262.546 270.271 255.969 C 272.736 248.486 270.703 242.217 263.831 236.968 C 255.895 233.368 249.512 233.988 244.587 238.718 Z M 266.078 74.647 C 271.286 69.852 272.628 61.199 269.171 54.978 C 265.778 48.875 258.105 45.732 251.172 47.607 C 244.002 49.546 239.606 55.504 239.723 63.126 C 239.905 75.061 250.167 81.082 263.336 76.585 C 264.463 75.802 265.353 75.314 266.078 74.647 Z M 184.728 163.897 C 190.93 168.038 197.744 166.649 205.044 160.455 C 211.716 154.795 219.199 151.627 228.154 151.813 C 239.472 152.049 250.839 152.431 262.111 151.665 C 277.882 150.593 292.419 152.877 304.958 163.231 C 305.586 163.749 306.369 164.371 307.109 164.412 C 311.426 164.648 316.141 165.888 319.989 164.6 C 326.962 162.266 329.639 155.97 330.037 148.886 C 330.494 140.731 328.168 133.605 320.723 129.383 C 314.167 125.666 308.043 128.525 302.911 132.592 C 294.196 139.5 284.563 142.608 273.505 142.327 C 262.356 142.044 251.174 141.859 240.043 142.388 C 225.647 143.071 212.73 140.374 201.063 131.113 C 192.221 124.094 182.241 127.55 177.908 138.105 C 175.49 143.994 175.631 150.045 178.041 156.352 C 180.382 159.121 182.123 162.157 184.728 163.897 Z"   />
  </svg>`
});
/**
 * The JupyterLab plugin for the GitLab Filebrowser.
 */
const fileBrowserPlugin = {
    id: PLUGIN_ID,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__.ISettingRegistry],
    activate: activateFileBrowser,
    autoStart: true
};
/**
 * Activate the file browser.
 */
function activateFileBrowser(app, palette, restorer, settingRegistry) {
    let widget = null;
    app.commands.addCommand(COMMAND_ID, {
        label: 'Open CPG Portal Files',
        execute: async () => {
            const drive = new _contents__WEBPACK_IMPORTED_MODULE_4__.CPGPortalDrive(app.docRegistry);
            if (settingRegistry) {
                const settings = await settingRegistry.load(PLUGIN_ID);
                console.log(settings);
                const baseUrl = settings.get('portalUrl').composite;
                const accessToken = settings.get('apiToken').composite;
                drive.baseUrl = baseUrl || _contents__WEBPACK_IMPORTED_MODULE_4__.DEFAULT_CPG_PORTAL_BASE_URL;
                drive.accessToken =
                    accessToken || window.localStorage.getItem('access_token');
            }
            // Create the widget if it doesn't exist.
            if (!widget || widget.isDisposed) {
                widget = new _CPGPortalFilesWidget__WEBPACK_IMPORTED_MODULE_5__.CPGPortalFilesWidget(app, drive);
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
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
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
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (fileBrowserPlugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.69862c80592236752e76.js.map