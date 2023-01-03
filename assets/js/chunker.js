// === divides document with divs by headings ===

// start rebuilding article
let new_inner = "";
let article = document.querySelector("article")

// all the headers in article except title
const toc_headings_depth = {{ .Site.Data.config.tocHeadingsDepth }}
console.log(toc_headings_depth)
let toc_headings_selector;
switch (toc_headings_depth) {
  case 1:
    toc_headings_selector = "article h1:not(.article-title)"
    break;
  case 2:
    toc_headings_selector = "article h1:not(.article-title), article h2"
    break;
  case 3:
    toc_headings_selector = "article h1:not(.article-title), article h2, article h3"
    break;
  case 4:
    toc_headings_selector = "article h1:not(.article-title), article h2, article h3, article h4"
    break;
  case 5:
    toc_headings_selector = "article h1:not(.article-title), article h2, article h3, article h4, article h5"
    break;
  default:
    toc_headings_selector = "article h1:not(.article-title), article h2, article h3, article h4, article h5, article h6"
}



let headers = document.querySelectorAll("article h1:not(.article-title), article h2, article h3, article h4, article h5, article h6")
let headersArr = Array.prototype.slice.call(headers)

// copy all things before first header ()
let child = article.firstElementChild
while (child != null && !(headersArr.includes(child.firstElementChild))) {
  new_inner = new_inner + child.outerHTML
  child = child.nextElementSibling
}

// for each header, wrap it in div and copy elements until next header
headers.forEach((header) => {
  let header_line = header.parentElement
  new_inner = new_inner + '<div class="text-chunk">'
  new_inner = new_inner + header.parentElement.outerHTML
  let tag = header_line.nextElementSibling
  while (tag != null && !(headersArr.includes(tag.firstElementChild))) {
    new_inner = new_inner + tag.outerHTML
    tag = tag.nextElementSibling
  }
  new_inner = new_inner + "</div>"
})

article.innerHTML = new_inner    
