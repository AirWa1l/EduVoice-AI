import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import ChatView from './ChatView.vue'

describe('ChatView', () => {
  const suggestions = ['¿Qué materias debo tomar este semestre?']

  it('shows welcome state when conversation is empty', () => {
    const wrapper = mount(ChatView, {
      props: {
        messages: [],
        suggestions,
        isEmpty: true,
        isRecording: false,
        isLoading: false,
        hasError: false,
        errorMessage: '',
      },
    })

    expect(wrapper.find('.welcome-state').exists()).toBe(true)
    expect(wrapper.find('.message-list').exists()).toBe(false)
  })

  it('shows message list when there are messages', () => {
    const wrapper = mount(ChatView, {
      props: {
        messages: [{ id: '1', role: 'user', text: 'Hola', time: '09:00' }],
        suggestions,
        isEmpty: false,
        isRecording: false,
        isLoading: false,
        hasError: false,
        errorMessage: '',
      },
    })

    expect(wrapper.find('.welcome-state').exists()).toBe(false)
    expect(wrapper.find('.message-list').exists()).toBe(true)
  })

  it('shows error banner and typing indicator according to props', () => {
    const wrapper = mount(ChatView, {
      props: {
        messages: [],
        suggestions,
        isEmpty: true,
        isRecording: false,
        isLoading: true,
        hasError: true,
        errorMessage: 'Error al procesar',
      },
    })

    expect(wrapper.find('.error-banner').exists()).toBe(true)
    expect(wrapper.find('.assistant-typing').exists()).toBe(true)
  })

  it('emits dismiss-error from error banner', async () => {
    const wrapper = mount(ChatView, {
      props: {
        messages: [],
        suggestions,
        isEmpty: true,
        isRecording: false,
        isLoading: false,
        hasError: true,
        errorMessage: 'Fallo de red',
      },
    })

    await wrapper.get('.error-banner__dismiss').trigger('click')

    expect(wrapper.emitted('dismiss-error')).toHaveLength(1)
  })
})
