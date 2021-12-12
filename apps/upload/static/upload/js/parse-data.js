// Parse CSV data into JSON using papaparse
function parsing(url) {
  Papa.parse(url, {
    download: true,
    header: true,
    beforeFirstChunk: function(chunk) {
      // Makes all header use the same names
      var rows = chunk.split(/\r\n|\r|\n/);
      var headings = rows[0].split(',');
      headings[0] = 'Date';
      headings[1] = 'Time';
      headings[2] = 'Open';
      headings[3] = 'High';
      headings[4] = 'Low';
      headings[5] = 'Close';
      rows[0] = headings.join();
      return rows.join('\n');
    },
    complete: function(results) {
      graphCandlestick(readyData(results.data));
    }
  });
}
