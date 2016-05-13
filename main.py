""" Main application module. """
import web
import urls

app = web.WebApp()
app.set_url_map(urls.url_map)

if __name__ == '__main__':

    from wsgiref.simple_server import make_server
    httpd = make_server('', 8000, app)
    print("Serving HTTP on port 8000...")
    httpd.handle_request()
    #httpd.serve_forever()
