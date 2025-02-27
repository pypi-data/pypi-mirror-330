import { MarkdownCell } from '@jupyterlab/cells';
import { Widget } from '@lumino/widgets';
import { Notebook } from '@jupyterlab/notebook';
import { ISettingRegistry } from '@jupyterlab/settingregistry';

export const E2X_METADATA_KEY = 'extended_cell';
export const E2X_GRADER_SETTINGS_CLASS = 'e2x_grader_options';
export const E2X_UNRENDER_BUTTON_CLASS = 'e2x_unrender';
export const E2X_BUTTON_CLASS = 'e2x_btn';

/**
 * Namespace containing interfaces and constants related to E2x metadata.
 */
export namespace E2xMetadata {
  /**
   * Interface representing the structure of E2x metadata.
   */
  export interface IE2xMetadata {
    /**
     * The type of the cell.
     * @default undefined
     */
    type?: string;

    /**
     * Additional options for the metadata.
     * @default {}
     */
    options?: any;
  }

  /**
   * Default values for E2x metadata.
   */
  export const E2X_METADATA_DEFAULTS: IE2xMetadata = {
    type: undefined,
    options: {}
  };
}

/**
 * Namespace containing private helper functions for E2xMarkdownCell.
 */
namespace Private {
  /**
   * Merges two objects, `objA` and `cleanMetadata`, ensuring that only the keys
   * present in `cleanMetadata` are included in the result. Additionally, it ensures
   * that the types of the values in `objA` match the types of the corresponding values
   * in `cleanMetadata` before assigning them.
   *
   * @template A - The type of the first object, which extends `Record<string, any>`.
   * @template B - The type of the second object, which extends `Record<string, any>`.
   *
   * @param objA - The first object to merge, containing potential values to override
   *               those in `cleanMetadata`.
   * @param cleanMetadata - The second object to merge, providing the keys and default
   *                        values for the result.
   *
   * @returns A new object that contains the keys from `cleanMetadata` with values
   *          from `objA` where the types match, otherwise the values from `cleanMetadata`.
   */
  export function mergeWithCleanMetadata<
    A extends Record<string, any>,
    B extends Record<string, any>
  >(objA: A, cleanMetadata: B): B {
    const result: Partial<B> = { ...cleanMetadata };

    // Iterate over the keys of cleanMetadata
    for (const key in cleanMetadata) {
      if (key in objA) {
        // Ensure the types match before assigning
        if (typeof objA[key] === typeof cleanMetadata[key]) {
          result[key] = objA[key];
        }
      }
    }

    return result as B;
  }
}

export namespace E2XMarkdownCell {
  export interface IOptions extends MarkdownCell.IOptions {
    settings?: ISettingRegistry.ISettings;
  }
}

/**
 * Represents an E2X Markdown cell, extending the functionality of a standard Markdown cell.
 * This class includes additional metadata handling, rendering logic, and grader section rendering.
 */
export class E2XMarkdownCell extends MarkdownCell {
  /**
   * Stores the last content of the cell as a string.
   * This is used to keep track of the previous state of the cell's content.
   *
   * @private
   */
  private __lastContent: string = '';

  private readonly _settings?: ISettingRegistry.ISettings;

  private _graderSection?: HTMLElement;

  /**
   * Constructs a new MarkdownCell instance.
   *
   * @param options - The options used to initialize the MarkdownCell.
   *
   * Initializes the MarkdownCell with the provided options, sets the
   * `showEditorForReadOnly` property to `false`, logs the current instance
   * to the console, and sets the metadata using the `cleanMetadata` method.
   */
  constructor(options: E2XMarkdownCell.IOptions) {
    super(options);
    this._settings = options.settings;
    if (this._settings) {
      this._settings.changed.connect(this.onSettingsUpdated, this);
    }
    this.showEditorForReadOnly = false;
    this.model.setMetadata(E2X_METADATA_KEY, this.cleanMetadata());
  }

  private get editMode(): boolean {
    if (this._settings) {
      return this._settings.get('edit_mode').composite as boolean;
    }
    return false;
  }

  private onSettingsUpdated(settings: ISettingRegistry.ISettings): void {
    if (this._graderSection) {
      this._graderSection.hidden = !(settings.get('edit_mode')
        .composite as boolean);
    }
  }

  /**
   * Gets the source content of the cell.
   * If the source content is not available, it returns a default string
   * indicating to type Markdown and LaTeX.
   *
   * @returns {string} The source content of the cell or a default string.
   */
  get source(): string {
    return (
      this.model?.sharedModel.getSource() || 'Type Markdown and LaTeX: $ a^2 $'
    );
  }

  /**
   * Checks if the content of the cell has changed since the last render.
   *
   * @returns {boolean} - Returns `true` if the content has changed, otherwise `false`.
   */
  private get contentChanged(): boolean {
    return this.__lastContent !== this.source;
  }

  /**
   * Retrieves the default metadata for E2x cells.
   *
   * @returns {Partial<E2xMetadata.IE2xMetadata>} The default metadata values.
   */
  protected get metadataDefaults(): Partial<E2xMetadata.IE2xMetadata> {
    return E2xMetadata.E2X_METADATA_DEFAULTS;
  }

  /**
   * Cleans the metadata by merging the current metadata with the default metadata.
   *
   * @template T - The type of the metadata that extends `E2xMetadata.IE2xMetadata`.
   * @returns A partial object of type `T` containing the cleaned metadata.
   */
  protected cleanMetadata<T extends E2xMetadata.IE2xMetadata>(): Partial<T> {
    return Private.mergeWithCleanMetadata(
      this.e2xMetadata,
      this.metadataDefaults
    ) as Partial<T>;
  }

  get e2xMetadata(): any {
    return this.model?.getMetadata(E2X_METADATA_KEY) || {};
  }

  get e2xCellType(): string | undefined {
    return this.e2xMetadata.type;
  }

  /**
   * Sets the e2x cell type and updates the notebook model accordingly.
   *
   * @param value - The new cell type to be set. It can be a string or undefined.
   *
   * When the cell type is changed, this method updates the cell's metadata field
   * with the new type, converts the current cell model to JSON, inserts a new cell
   * with the updated model at the next index, and deletes the old cell.
   */
  set e2xCellType(value: string | undefined) {
    const oldCellType = this.e2xCellType;
    if (value !== oldCellType) {
      this.setE2xMetadataField('type', value);
      const model = this.model.toJSON();
      const index = this.cellIndex;
      this.notebook.model?.sharedModel.insertCell(index + 1, model);
      this.notebook.model?.sharedModel.deleteCell(index);
    }
  }

  public getE2xMetadataField(field: string, default_value: any = {}): any {
    return this.e2xMetadata?.[field] ?? default_value;
  }

  public setE2xMetadataField(field: string, value: any): void {
    const metadata = this.e2xMetadata;
    metadata[field] = value;
    this.model?.setMetadata(E2X_METADATA_KEY, metadata);
  }

  /**
   * Waits for the render of a widget to complete within a specified timeout.
   *
   * This method checks if the widget's node contains a child element with the class
   * 'jp-RenderedMarkdown'. If the element is found, it resolves the promise with the widget.
   * If not, it continues to check at intervals defined by the timeout parameter.
   *
   * @param widget - The widget to wait for rendering.
   * @param timeout - The interval in milliseconds to wait between checks.
   * @returns A promise that resolves with the widget once it has rendered.
   */
  protected _waitForRender(widget: Widget, timeout: number): Promise<Widget> {
    return new Promise<Widget>(resolve => {
      function waitReady() {
        const firstChild = widget.node.querySelector('.jp-RenderedMarkdown *');
        if (firstChild) {
          resolve(widget);
        } else {
          setTimeout(waitReady, timeout);
        }
      }
      waitReady();
    });
  }

  /**
   * Renders the input widget and performs additional operations after rendering.
   *
   * This method sets the cell to read-only mode, calls the superclass's renderInput method,
   * and then checks if the content has changed. If the content has changed, it waits for the
   * rendering to complete and then performs post-render operations including rendering the
   * grader section.
   *
   * @param widget - The widget to be rendered.
   */
  protected renderInput(widget: Widget): void {
    this.readOnly = true;
    super.renderInput(widget);
    if (this.contentChanged) {
      this._waitForRender(widget, 2).then((widget: Widget) => {
        this.postRender(widget);
        this.renderGraderSection(widget);
      });
      this.__lastContent = this.source;
    }
  }

  /**
   * This method is called after the widget has been rendered.
   * It is intended to be overridden by subclasses to perform
   * any post-rendering operations. The default implementation
   * does nothing.
   *
   * @param widget - The widget that has been rendered.
   */
  protected postRender(widget: Widget): void {
    // Intentionally left empty
  }

  /**
   * Renders the grader section for the E2XMarkdownCell.
   *
   * This method creates a grader section with a horizontal rule and an "Edit Cell" button,
   * and appends it to the provided widget's HTML node. The "Edit Cell" button, when clicked,
   * sets the cell to be editable and not rendered.
   *
   * @param widget - The widget to which the grader section will be appended.
   */
  private renderGraderSection(widget: Widget): void {
    if (!this.e2xCellType) {
      return;
    }
    const html = widget.node;
    const grader = document.createElement('div');
    grader.appendChild(document.createElement('hr'));
    grader.className = E2X_GRADER_SETTINGS_CLASS;
    const unrenderButton = document.createElement('button');
    unrenderButton.classList.add(E2X_UNRENDER_BUTTON_CLASS, E2X_BUTTON_CLASS);
    unrenderButton.textContent = 'Edit Cell';
    unrenderButton.onclick = () => {
      this.readOnly = false;
      this.rendered = false;
    };
    grader.appendChild(unrenderButton);
    this._graderSection = grader;
    if (!this.editMode) {
      grader.hidden = true;
    }
    html.appendChild(grader);
  }

  protected get notebook(): Notebook {
    return this.parent as Notebook;
  }

  protected get cellIndex(): number {
    return this.notebook.widgets.findIndex(widget => widget === this);
  }
}
