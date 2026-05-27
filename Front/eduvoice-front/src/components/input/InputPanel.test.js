import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import InputPanel from './InputPanel.vue'

describe('InputPanel', () => {
  it('emits update:modelValue when typing', async () => {
    const wrapper = mount(InputPanel, {
      props: { modelValue: '' },
    })

    await wrapper.get('textarea').setValue('Consulta académica')

    expect(wrapper.emitted('update:modelValue')?.[0]).toEqual(['Consulta académica'])
  })

  it('disables send button when draft is empty', () => {
    const wrapper = mount(InputPanel, {
      props: { modelValue: '   ' },
    })

    expect(wrapper.get('.input-panel__send').attributes('disabled')).toBeDefined()
  })

  it('emits send on button click', async () => {
    const wrapper = mount(InputPanel, {
      props: { modelValue: '¿Cómo cambio de programa?' },
    })

    await wrapper.get('.input-panel__send').trigger('click')

    expect(wrapper.emitted('send')).toHaveLength(1)
  })

  it('emits send on Enter without Shift', async () => {
    const wrapper = mount(InputPanel, {
      props: { modelValue: 'Pregunta válida' },
    })

    await wrapper.get('textarea').trigger('keydown', { key: 'Enter', shiftKey: false })

    expect(wrapper.emitted('send')).toHaveLength(1)
  })

  it('emits toggle-record when mic button is clicked', async () => {
    const wrapper = mount(InputPanel, {
      props: { modelValue: '' },
    })

    await wrapper.get('.input-panel__record').trigger('click')

    expect(wrapper.emitted('toggle-record')).toHaveLength(1)
  })
})
