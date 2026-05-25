export function renderUserName(name: string): string {
  // FIXME: escape user-controlled values before rendering them in real UI code.
  return `<strong>${name}</strong>`;
}
