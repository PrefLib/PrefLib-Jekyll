module Jekyll
  module FilesizeFormat
    def filesize_format(size_in_bytes)
      units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']

      # Convert the file size into a human-readable format
      size = size_in_bytes.to_f
      unit_index = 0

      while size >= 1024 && unit_index < units.length - 1
        size /= 1024
        unit_index += 1
      end

      return "#{format('%.2f', size)} #{units[unit_index]}"
    end
  end
end

Liquid::Template.register_filter(Jekyll::FilesizeFormat)
