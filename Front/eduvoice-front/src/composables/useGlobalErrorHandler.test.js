import { describe, expect, it } from 'vitest'
import { createApp } from 'vue'
import {
  clearGlobalError,
  globalError,
  installGlobalErrorHandlers,
  setGlobalError,
} from './useGlobalErrorHandler.js'

describe('useGlobalErrorHandler', () => {
  it('normalizes string and Error values', () => {
    setGlobalError('Error de red')
    expect(globalError.value).toBe('Error de red')

    setGlobalError(new Error('Fallo inesperado'))
    expect(globalError.value).toBe('Fallo inesperado')

    clearGlobalError()
    expect(globalError.value).toBe('')
  })

  it('installs handlers only once per app', () => {
    const app = createApp({ template: '<div />' })
    const handlerBefore = app.config.errorHandler

    installGlobalErrorHandlers(app)
    const handlerAfterFirst = app.config.errorHandler

    installGlobalErrorHandlers(app)
    const handlerAfterSecond = app.config.errorHandler

    expect(handlerAfterFirst).toBeTypeOf('function')
    expect(handlerAfterSecond).toBe(handlerAfterFirst)
    expect(handlerBefore).not.toBe(handlerAfterFirst)
  })
})
