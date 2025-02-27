import { NotebookPanel } from '@jupyterlab/notebook';
import { Cell, MarkdownCell } from '@jupyterlab/cells';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { E2XMarkdownCell } from './cell';
import {
  E2X_MULTIPLECHOICE_CELL_TYPE,
  E2X_SINGLECHOICE_CELL_TYPE,
  MultipleChoiceCell,
  SingleChoiceCell
} from './choicecell';

export class E2XContentFactory extends NotebookPanel.ContentFactory {
  private readonly _settings: ISettingRegistry.ISettings | undefined;

  constructor(
    options: Cell.ContentFactory.IOptions,
    settings?: ISettingRegistry.ISettings
  ) {
    super(options);
    this._settings = settings;
  }
  createMarkdownCell(options: E2XMarkdownCell.IOptions): MarkdownCell {
    if (!options.contentFactory) {
      options.contentFactory = this;
    }
    options.settings = this._settings;
    const e2xCellType = options.model.getMetadata('extended_cell')?.type;
    if (e2xCellType === E2X_MULTIPLECHOICE_CELL_TYPE) {
      return new MultipleChoiceCell(options);
    } else if (e2xCellType === E2X_SINGLECHOICE_CELL_TYPE) {
      return new SingleChoiceCell(options);
    }
    const cell = new E2XMarkdownCell(options);
    return cell;
  }
}
