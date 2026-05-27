import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import ErrorBanner from './ErrorBanner.vue'

describe('ErrorBanner', () => {
  it('renders the error message', () => {
    const wrapper = mount(ErrorBanner, {
      props: { message: 'No se pudo conectar con el servidor' },
    })

    expect(wrapper.get('[role="alert"]').text()).toContain('No se pudo conectar con el servidor')
  })

  it('emits dismiss when close button is clicked', async () => {
    const wrapper = mount(ErrorBanner, {
      props: { message: 'Error de validación' },
    })

    await wrapper.get('button').trigger('click')

    expect(wrapper.emitted('dismiss')).toHaveLength(1)
  })
})
