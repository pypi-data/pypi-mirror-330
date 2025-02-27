import { Widget } from '@lumino/widgets';
import { E2XMarkdownCell, E2xMetadata } from './cell';

const E2X_MULTIPLECHOICE_FORM_CLASS = 'e2x-multiplechoice-form';
const E2X_SINGLECHOICE_FORM_CLASS = 'e2x-singlechoice-form';

export const E2X_MULTIPLECHOICE_CELL_TYPE = 'multiplechoice';
export const E2X_SINGLECHOICE_CELL_TYPE = 'singlechoice';

export namespace ChoiceCellMetadata {
  export interface IMultipleChoiceMetadata extends E2xMetadata.IE2xMetadata {
    choice: string[];
    num_of_choices: number;
  }

  export const MULTIPLECHOICE_METADATA_DEFAULTS: IMultipleChoiceMetadata = {
    ...E2xMetadata.E2X_METADATA_DEFAULTS,
    type: E2X_MULTIPLECHOICE_CELL_TYPE,
    choice: [],
    num_of_choices: 0
  };

  export interface ISingleChoiceMetadata extends E2xMetadata.IE2xMetadata {
    choice: string;
  }

  export const SINGLECHOICE_METADATA_DEFAULTS: ISingleChoiceMetadata = {
    ...E2xMetadata.E2X_METADATA_DEFAULTS,
    type: E2X_SINGLECHOICE_CELL_TYPE,
    choice: ''
  };
}

export class ChoiceCell extends E2XMarkdownCell {
  get choices(): string[] {
    return this.getE2xMetadataField('choice', []);
  }
  set choices(choices: string[]) {
    this.setE2xMetadataField('choice', choices);
  }
}

export class MultipleChoiceCell extends ChoiceCell {
  get choiceCount(): number {
    return this.getE2xMetadataField('num_of_choices', 0);
  }

  set choiceCount(value: number) {
    this.setE2xMetadataField('num_of_choices', value);
  }

  protected get metadataDefaults(): ChoiceCellMetadata.IMultipleChoiceMetadata {
    return ChoiceCellMetadata.MULTIPLECHOICE_METADATA_DEFAULTS;
  }

  addChoice(choice: string): void {
    const choices = this.choices;
    if (!choices.includes(choice)) {
      choices.push(choice);
      this.choices = choices;
    }
  }

  removeChoice(choice: string): void {
    const choices = this.choices;
    const index = choices.indexOf(choice);
    if (index >= 0) {
      choices.splice(index, 1);
      this.choices = choices;
    }
  }

  createChoiceElement(value: string, selected: boolean): HTMLInputElement {
    const choice = document.createElement('input');
    choice.type = 'checkbox';
    choice.name = this.model.id;
    choice.value = value;
    choice.checked = selected;
    choice.onchange = event => {
      const elem = event.target as HTMLInputElement;
      if (elem.checked) {
        this.addChoice(value);
      } else {
        this.removeChoice(value);
      }
    };
    return choice;
  }

  protected postRender(widget: Widget): void {
    const html = widget.node;
    const lists = html.querySelectorAll('ul');
    if (lists.length === 0) {
      return;
    }
    const list = lists[0];
    const items = list.querySelectorAll('li');
    const form = document.createElement('form');
    form.classList.add(E2X_MULTIPLECHOICE_FORM_CLASS);
    if (this.choiceCount !== items.length) {
      this.choiceCount = items.length;
      this.choices = [];
    }
    items.forEach((item, index) => {
      const input = this.createChoiceElement(
        index.toString(),
        this.choices.includes(index.toString())
      );
      const label = document.createElement('label');
      label.innerHTML = item.innerHTML;
      form.appendChild(input);
      form.appendChild(label);
      form.appendChild(document.createElement('br'));
    });
    list.replaceWith(form);
  }
}

export class SingleChoiceCell extends ChoiceCell {
  get choice(): string {
    return this.getE2xMetadataField('choice', '');
  }

  set choice(choice: string) {
    this.setE2xMetadataField('choice', choice);
  }

  protected get metadataDefaults(): Partial<ChoiceCellMetadata.ISingleChoiceMetadata> {
    return ChoiceCellMetadata.SINGLECHOICE_METADATA_DEFAULTS;
  }

  createChoiceElement(value: string, selected: boolean): HTMLInputElement {
    const choice = document.createElement('input');
    choice.type = 'radio';
    choice.name = this.model.id;
    choice.value = value;
    choice.checked = selected;
    choice.onchange = event => {
      const elem = event.target as HTMLInputElement;
      if (elem.checked) {
        this.choice = value;
      }
    };
    return choice;
  }

  protected postRender(widget: Widget): void {
    const html = widget.node;
    const lists = html.querySelectorAll('ul');
    if (lists.length === 0) {
      return;
    }
    const list = lists[0];
    const items = list.querySelectorAll('li');
    const form = document.createElement('form');
    form.classList.add(E2X_SINGLECHOICE_FORM_CLASS);
    if (this.choice !== '' && parseInt(this.choice) >= items.length) {
      this.choice = '';
    }
    items.forEach((item, index) => {
      const input = this.createChoiceElement(
        index.toString(),
        this.choice === index.toString()
      );
      const label = document.createElement('label');
      label.innerHTML = item.innerHTML;
      form.appendChild(input);
      form.appendChild(label);
      form.appendChild(document.createElement('br'));
    });
    list.replaceWith(form);
  }
}
