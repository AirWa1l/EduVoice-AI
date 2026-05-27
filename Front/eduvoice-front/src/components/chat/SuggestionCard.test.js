import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import SuggestionCard from './SuggestionCard.vue'

describe('SuggestionCard', () => {
  it('renders suggestion text', () => {
    const wrapper = mount(SuggestionCard, {
      props: { text: '¿Cómo mejoro mi rendimiento académico?' },
    })

    expect(wrapper.text()).toContain('¿Cómo mejoro mi rendimiento académico?')
  })

  it('emits select with suggestion text on click', async () => {
    const wrapper = mount(SuggestionCard, {
      props: { text: '¿Qué requisitos necesito para graduarme?' },
    })

    await wrapper.trigger('click')

    expect(wrapper.emitted('select')?.[0]).toEqual(['¿Qué requisitos necesito para graduarme?'])
  })
})
