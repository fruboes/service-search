import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

import Backend from 'i18next-http-backend';
import LanguageDetector from 'i18next-browser-languagedetector';


// Likely this could be achieved in more elegent way..
const request = new XMLHttpRequest();
request.open("GET", "/fallbackLocale", false);
request.send(null);

let fallbackLocale = "en";
if (request.status === 200) {
  let data = JSON.parse(request.responseText)
  fallbackLocale = data.lang;
} else {
  console.log("Failed obtaining fallback locale", request);
}

i18n
  // load translation using http -> see /public/locales (i.e. https://github.com/i18next/react-i18next/tree/master/example/react/public/locales)
  // learn more: https://github.com/i18next/i18next-http-backend
  // want your translations to be loaded from a professional CDN? => https://github.com/locize/react-tutorial#step-2---use-the-locize-cdn
  .use(Backend)
  // detect user language
  // learn more: https://github.com/i18next/i18next-browser-languageDetector
  .use(LanguageDetector)
  // pass the i18n instance to react-i18next.
  .use(initReactI18next)
  // init i18next
  // for all options read: https://www.i18next.com/overview/configuration-options
  .init({
    fallbackLng: fallbackLocale,
    debug: true,

    interpolation: {
      escapeValue: false, // not needed for react as it escapes by default
    },
    // https://github.com/i18next/i18next-browser-languageDetector
    //  note: we dont use localStorage/sessionStorage for detection, as it is also used as cache
    //        (with the same key name). This leads to a weird behavior when multiple tabs
    //        with different language settings are used
    detection: {
      order: ['querystring', 'cookie', 'navigator'],
    }
  });

export default i18n;
