// todo:
export function download_csv(file_name, csv_header, csv_content_array) {}

export function replacer(key, value) {
  // Filtering out properties
  if (typeof value === 'object') {
    return undefined;
  }
  return value;
}
