import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import UserMessage from './UserMessage.vue'

describe('UserMessage', () => {
  it('renders user text and time', () => {
    const wrapper = mount(UserMessage, {
      props: {
        text: '¿Cuáles son los requisitos de grado?',
        time: '10:30',
      },
    })

    expect(wrapper.find('.user-message__text').text()).toBe('¿Cuáles son los requisitos de grado?')
    expect(wrapper.find('time').text()).toBe('10:30')
  })
})
