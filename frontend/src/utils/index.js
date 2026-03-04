 import {} from './is'
export function awaitWrapper(promise) {
  return promise.then((res) => [null, res]).catch((err) => [err, null])
}