const userPref = window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark'
const currentTheme = localStorage.getItem('theme') ?? userPref
const syntaxTheme = document.querySelector("#theme-link");

{{ $darkSyntax := resources.Get "styles/_dark_syntax.scss" | resources.ToCSS (dict "outputStyle" "compressed") | resources.Fingerprint "md5" | resources.Minify  }}
{{ $lightSyntax := resources.Get "styles/_light_syntax.scss" | resources.ToCSS (dict "outputStyle" "compressed") | resources.Fingerprint "md5" | resources.Minify  }}

if (currentTheme) {
  document.documentElement.setAttribute('saved-theme', currentTheme);
  syntaxTheme.href = currentTheme === 'dark' ?  '{{ relURL $darkSyntax.Permalink }}' :  '{{ relURL $lightSyntax.Permalink }}';
}

const switchTheme = () => {
  var currentTheme = document.documentElement.getAttribute("saved-theme");

  if (currentTheme === "light") {
    document.documentElement.setAttribute('saved-theme', 'dark')
    localStorage.setItem('theme', 'dark');
    syntaxTheme.href = '{{ relURL $darkSyntax.Permalink }}';

  } else {
    document.documentElement.setAttribute('saved-theme', 'light')
    localStorage.setItem('theme', 'light')
    syntaxTheme.href = '{{ relURL $lightSyntax.Permalink }}';
  }
}

window.addEventListener('DOMContentLoaded', () => {
  document.querySelector('#toggle-label-light').addEventListener('click', switchTheme, false)
  document.querySelector('#toggle-label-dark').addEventListener('click', switchTheme, false)
})
