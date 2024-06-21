/**
 * Capitalise the first letter of the given text and return in a new string.
 *
 * @param {string} text
 * @returns {string} a new string with a capital first letter
 */
export function capitalise(text) {
  return `${text.charAt(0).toUpperCase()}${text.slice(1)}`;
}
