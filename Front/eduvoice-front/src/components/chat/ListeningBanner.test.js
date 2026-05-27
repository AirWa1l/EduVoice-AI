import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import ListeningBanner from './ListeningBanner.vue'

describe('ListeningBanner', () => {
  it('renders listening status text', () => {
    const wrapper = mount(ListeningBanner)

    expect(wrapper.attributes('role')).toBe('status')
    expect(wrapper.text()).toContain('Escuchando...')
    expect(wrapper.text()).toContain('Habla claramente tu pregunta')
  })
})
