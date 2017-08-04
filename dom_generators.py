#coding: utf-8
import hsl_transit_info
import weather_forecast

if __name__ == '__main__': # Local Pythonista test
  import ui, os, objc_util
  v = ui.WebView()
  v.present('full_screen', hide_title_bar=True)
  
  #[[NSURLCache sharedURLCache] removeAllCachedResponses];
  NSURLCache = objc_util.ObjCClass('NSURLCache')
  url_cache = NSURLCache.sharedURLCache()
  url_cache.removeAllCachedResponses()
  
  def set_module(view, location, html_string):
    js = "wrapper = selectWrapper('%s'); wrapper.innerHTML = `%s`;" % (location, html_string)
    view.eval_js(js)
  
  class LoadDelegate():
    def webview_did_finish_load(self, webview):
      temp_now = 19
      forecast_html = weather_forecast.get_html(19)
      set_module(webview, 'region top right', forecast_html)
      
      set_module(webview, 'region bottom right', hsl_transit_info.get_html())
      
  v.delegate = LoadDelegate()
  v.load_url(os.path.abspath('index.html'))
  #v.load_html(weather_forecast.get_html())
  
