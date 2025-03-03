// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

import { Signal, ISignal } from '@lumino/signaling';

import { URLExt } from '@jupyterlab/coreutils';

import { DocumentRegistry } from '@jupyterlab/docregistry';
import { ObservableValue } from '@jupyterlab/observables';

import { Contents, ServerConnection } from '@jupyterlab/services';

import { ICPGPortalContents } from './cpgportal';

export const DEFAULT_CPG_PORTAL_BASE_URL = 'https://portal.cpg.unimelb.edu.au';

/**
 * A Contents.IDrive implementation that serves as a read-only
 * view onto GitLab repositories.
 */
export class CPGPortalDrive implements Contents.IDrive {
  /**
   * Construct a new drive object.
   *
   * @param options - The options used to initialize the object.
   */
  constructor(registry: DocumentRegistry) {
    this._serverSettings = ServerConnection.makeSettings();
    this.baseUrl = DEFAULT_CPG_PORTAL_BASE_URL;
    this.errorState = new ObservableValue(false);
  }

  /**
   * The name of the drive.
   */
  get name(): 'CPG Portal' {
    return 'CPG Portal';
  }

  /**
   * State for whether the user is valid.
   */
  get validToken(): boolean {
    return this._validToken;
  }

  /**
   * Settings for the notebook server.
   */
  get serverSettings(): ServerConnection.ISettings {
    return this._serverSettings;
  }

  /**
   * State for whether the drive is being rate limited by GitLab.
   */
  readonly errorState: ObservableValue;

  /**
   * A signal emitted when a file operation takes place.
   */
  get fileChanged(): ISignal<Contents.IDrive, Contents.IChangedArgs> {
    return this._fileChanged;
  }

  /**
   * Test whether the manager has been disposed.
   */
  get isDisposed(): boolean {
    return this._isDisposed;
  }

  /**
   * Dispose of the resources held by the manager.
   */
  dispose(): void {
    if (this.isDisposed) {
      return;
    }
    this._isDisposed = true;
    Signal.clearData(this);
  }

  /**
   * The GitLab base URL
   */
  get baseUrl(): string {
    return this._baseUrl;
  }

  /**
   * The GitLab base URL is set by the settingsRegistry change hook
   */
  set baseUrl(url: string) {
    this._baseUrl = url;
  }

  /**
   * The GitLab access token
   */
  get accessToken(): string | null | undefined {
    return this._accessToken;
  }

  /**
   * The GitLab access token is set by the settingsRegistry change hook
   */
  set accessToken(token: string | null | undefined) {
    this._accessToken = token;
  }

  // Minimal implementation of 'get' to fetch a directory model.
  async get(
    path: string,
    options?: Contents.IFetchOptions
  ): Promise<Contents.IModel> {
    const url = URLExt.join(this.baseUrl, 'api', 'v1', 'files');
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
    const data: ICPGPortalContents = await response.json();
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

  async getDownloadUrl(path: string): Promise<string> {
    return URLExt.join(this.baseUrl, 'api', 'v1', 'files', path, 'download');
  }

  /**
   * Create a new untitled file or directory in the specified directory path.
   *
   * @param options: The options used to create the file.
   *
   * @returns A promise which resolves with the created file content when the
   *    file is created.
   */
  newUntitled(options: Contents.ICreateOptions = {}): Promise<Contents.IModel> {
    return Promise.reject('Repository is read only');
  }

  /**
   * Delete a file.
   *
   * @param path - The path to the file.
   *
   * @returns A promise which resolves when the file is deleted.
   */
  delete(path: string): Promise<void> {
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
  rename(path: string, newPath: string): Promise<Contents.IModel> {
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
  save(
    path: string,
    options: Partial<Contents.IModel>
  ): Promise<Contents.IModel> {
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
  copy(fromFile: string, toDir: string): Promise<Contents.IModel> {
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
  createCheckpoint(path: string): Promise<Contents.ICheckpointModel> {
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
  listCheckpoints(path: string): Promise<Contents.ICheckpointModel[]> {
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
  restoreCheckpoint(path: string, checkpointID: string): Promise<void> {
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
  deleteCheckpoint(path: string, checkpointID: string): Promise<void> {
    return Promise.reject('Read only');
  }

  private _baseUrl = '';
  private _accessToken: string | null | undefined;
  private _validToken = false;
  private _serverSettings: ServerConnection.ISettings;
  private _isDisposed = false;
  private _fileChanged = new Signal<this, Contents.IChangedArgs>(this);
}

/**
 * Specification for a file in a repository.
 */
export interface IGitLabResource {
  /**
   * The user or group for the resource.
   */
  readonly user: string;

  /**
   * The repository in the group/user.
   */
  readonly repository: string;

  /**
   * The path in the repository to the resource.
   */
  readonly path: string;
}
