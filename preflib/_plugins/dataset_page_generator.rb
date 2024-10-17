
module Jekyll
  class DataSetPage < Page
    def initialize(site, base, dir, name, dataset)
      @site = site
      @base = base
      @dir = dir
      @name = name

      self.process(@name)
      self.data ||= {}
      self.data['layout'] = 'dataset'
      self.data['dataset'] = dataset
      self.data['title'] = "Preflib | #{dataset['name']}"
    end
  end

  class DatasetPageGenerator < Generator
    safe true

    def generate(site)
      datasets = site.data['datasets']

      datasets.each do |dataset|
        dataset_page = DataSetPage.new(site, site.source, 'dataset', "#{dataset['series_number']}.html", dataset)
        site.pages << dataset_page
      end
    end
  end
end