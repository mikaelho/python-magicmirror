#coding: utf-8
import hsl_transit_info
import weather_forecast
import calendar_entries

if __name__ == '__main__': # Local Pythonista test
  import ui, os, objc_util
  
  class WebContainer(ui.View):
    
    def __init__(self):
      self.v = ui.WebView()
      self.v.flex = 'WH'
      self.add_subview(self.v)
    
    def will_close(self):
      self.v.load_html('<html><body></body></html>')
      NSURLCache = objc_util.ObjCClass('NSURLCache')
      url_cache = NSURLCache.sharedURLCache()
      url_cache.removeAllCachedResponses()
  
  c = WebContainer()

  c.present('full_screen', hide_title_bar=True)
  
  def set_module(view, location, html_string):
    js = "wrapper = selectWrapper('%s'); wrapper.innerHTML = `%s`;" % (location, html_string)
    view.eval_js(js)
  
  class LoadDelegate():
    def webview_did_finish_load(self, webview):
      temp_now = 19
      forecast_html = weather_forecast.get_html(19)
      set_module(webview, 'region top right', forecast_html)
      
      set_module(webview, 'region bottom right', hsl_transit_info.get_html())
      
      set_module(webview, 'region top left', calendar_entries.get_html())
      
  c.v.delegate = LoadDelegate()
  c.v.load_url(os.path.abspath('index.html'))
  #v.load_html(weather_forecast.get_html())
  
