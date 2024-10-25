require 'open-uri'
require 'openssl'
require 'fileutils'
require 'digest'

Jekyll::Hooks.register :site, :pre_render do |site|
  url = "https://raw.githubusercontent.com/PrefLib/PrefLib-Data/main/FORMAT_SPECIFICATION.md"
  destination_path = "_includes/FORMAT_SPECIFICATION.md"

  # Ensure the _includes directory exists
  FileUtils.mkdir_p(File.dirname(destination_path))

  # Fetch the remote file and calculate its checksum
  begin
    remote_content = URI.open(url, { ssl_verify_mode: OpenSSL::SSL::VERIFY_NONE }).read
    remote_checksum = Digest::SHA256.hexdigest(remote_content)

    # Check if the local file exists
    if File.exist?(destination_path)
      local_content = File.read(destination_path)
      local_checksum = Digest::SHA256.hexdigest(local_content)

      # Only overwrite if the checksums are different
      if remote_checksum != local_checksum
        File.open(destination_path, "wb") do |output|
          output.write(remote_content)
        end
        puts "Updated FORMAT_SPECIFICATION.md."
      else
        puts "FORMAT_SPECIFICATION.md is up-to-date."
      end
    else
      # File doesn't exist, so create it
      File.open(destination_path, "wb") do |output|
        output.write(remote_content)
      end
      puts "Downloaded FORMAT_SPECIFICATION.md."
    end

  rescue StandardError => e
    puts "Error fetching FORMAT_SPECIFICATION.md: #{e.message}"
  end
end
