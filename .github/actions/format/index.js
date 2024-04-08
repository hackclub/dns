const core = require("@actions/core")
const fs = require("fs")
const yaml = require("js-yaml")

try {
  const yamlFiles = fs.readdirSync("./").filter(file => file.endsWith(".yaml"))
  format(yamlFiles)
} catch (error) {
  core.setFailed(error.message)
}

function format(yamlFiles) {
  yamlFiles.forEach(file => {
    const content = fs.readFileSync(file)

    let data = yaml.load(content)
    data = consistent(data)
    data = sort(data)

    const formattedContent = yaml.dump(data, {quotingType: '"', lineWidth: -1})
    fs.writeFileSync(file, formattedContent)
  })
}

function consistent(data) { // one-record subdomains might not be an array
  for (const key in data) {
    if (!Array.isArray(data[key])) {
      const array = [data[key]]
      data[key] = array
    }
  }

  return data
}

function sort(subdomains) {
  const sortedSubdomains = {}
  Object.keys(subdomains).sort().forEach(key => {
    sortedSubdomains[key] = subdomains[key]
  })

  for (const subdomain in sortedSubdomains) {
    const records = sortedSubdomains[subdomain]
    for (const record in records) {
      const sortedOptions = {}
      Object.keys(records[record]).sort().forEach(option => {
        sortedOptions[option] = sortedSubdomains[subdomain][record][option]
      })
      sortedSubdomains[subdomain][record] = sortedOptions
    }
  }

  return sortedSubdomains
}
