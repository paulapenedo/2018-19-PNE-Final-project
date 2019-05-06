import http.server
import socketserver
import termcolor

from link import ELink

# Define the Server's port
PORT = 8000

eLink = ELink()

class MainHandler(http.server.BaseHTTPRequestHandler):

    def error_page(self):
        f = open("error.html", 'r')
        return f.read()

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        result = '0'

        if self.path == "/":
            f = open("main_page.html", 'r')
            contents = f.read()
            f.close()
        else:
            result = ''

            contents = """<!DOCTYPE html>
                                    <html lang ="en">
                                    <head>
                                        <meta charset="UTF-8">
                                        <title>SERVER RESPONSE</title>
                                    </head>
                                    <body style="background-color: lightgreen">"""

            page_end = """<br> <a href="/"> [Main page] </a>
                                </body></html>"""

            args = self.path.split('?')
            if len(args) > 1:
                args = args[1].split('&')

            if '/listSpecies' in self.path:
                result = self.listSpecies(args)

            elif '/karyotype' in self.path:
                result = self.karyotype(args)

            elif '/chromosomeLength' in self.path:
                result = self.chromLength(args)

            contents = contents + result + page_end

        if result == '':
            contents = self.error_page()

        # Generating the response message
        self.send_response(200)  # -- Status line: OK!

        # Define the content-type header:
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(str.encode(contents)))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(str.encode(contents))

        return

    def listSpecies(self, args):
        value = args[0].split('=')

        limit = 0
        if value[1] is not '':
            try:
                limit = int(value[1])
            except:
                return ''

        species = eLink.list_species(limit)

        return self.table_from_list(species, "Species name")

    def karyotype(self, args):
        value = args[0].split('=')

        specie = value[1]
        if specie is not '':
            try:
                karyotype = eLink.karyotype(specie)

                return self.table_from_list(karyotype, "Karyotype of " + specie)
            except:
                return ''

    def chromLength(self, args):
        specie = args[0].split('=')[1]
        chromo = args[1].split('=')[1]

        if specie is '' or chromo is '':
            return ''
        else:
            length = eLink.chromosome_Length(specie, chromo)

            if length <= 0:
                return "Chromosome not found"
            else:
                return self.table_from_list([length], "Chromosome " + chromo)

    def table_from_list(self, list, header):
        table = """
                <table border = 1>
                   <tbody>
                        <th> """ + header + "</th>"
        for k in list:
            table = table + "<tr><td>" + str(k) + "</td></tr>"

        return table + "</tbody></table>"

# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
Handler = MainHandler

# -- Open the socket server
socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()

print("")
print("Server Stopped")