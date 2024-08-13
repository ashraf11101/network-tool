#include <iostream>
#include <boost/asio.hpp>

using namespace boost::asio;
using namespace boost::asio::ip;

void handle_client(tcp::socket& socket) {
    try {
        for (;;) {
            char data[1024];
            boost::system::error_code error;

            // Read data from the client
            size_t length = socket.read_some(buffer(data), error);
            if (error == boost::asio::error::eof)
                break; // Connection closed cleanly by peer
            else if (error)
                throw boost::system::system_error(error); // Some other error

            // Print received data
            std::cout << "Received from " << socket.remote_endpoint() << ": ";
            std::cout.write(data, length);
            std::cout << std::endl;
        }
    } catch (std::exception& e) {
        std::cerr << "Exception in thread: " << e.what() << std::endl;
    }
}

int main() {
    try {
        io_context io_context;

        // Get all available interfaces and their addresses
        tcp::resolver resolver(io_context);
        tcp::resolver::query query("", "");
        tcp::resolver::iterator endpoints = resolver.resolve(query);

        // Create and bind sockets for each interface
        for (tcp::endpoint endpoint : endpoints) {
            tcp::acceptor acceptor(io_context);
            acceptor.open(endpoint.protocol());
            acceptor.set_option(socket_base::reuse_address(true));
            acceptor.bind(endpoint);
            acceptor.listen();

            std::cout << "Listening on " << endpoint << std::endl;

            // Accept connections and handle clients
            for (;;) {
                tcp::socket socket(io_context);
                acceptor.accept(socket);
                std::cout << "Accepted connection from: " << socket.remote_endpoint() << std::endl;

                std::thread(handle_client, std::ref(socket)).detach();
            }
        }
    } catch (std::exception& e) {
        std::cerr << "Exception: " << e.what() << std::endl;
    }

    return 0;
}
