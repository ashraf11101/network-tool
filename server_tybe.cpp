#include <iostream>
#include <curl/curl.h>
#include <string>

// بناء نص URL للحصول على معلومات النظام باستخدام عنوان IP
std::string buildUrl(const std::string& ip) {
    return "http://ip-api.com/json/" + ip;
}

// دالة callback لمعالجة البيانات المستردة من الاستجابة
size_t writeCallback(void* contents, size_t size, size_t nmemb, std::string* buffer) {
    size_t realSize = size * nmemb;
    buffer->append((char*)contents, realSize);
    return realSize;
}

// دالة لجلب معلومات النظام باستخدام عنوان IP
std::string getSystemInfo(const std::string& ip) {
    CURL* curl;
    CURLcode res;
    std::string readBuffer;

    curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, buildUrl(ip).c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, writeCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        res = curl_easy_perform(curl);
        curl_easy_cleanup(curl);

        if (res == CURLE_OK) {
            return readBuffer;
        } else {
            return "Failed to retrieve information.";
        }
    } else {
        return "Failed to initialize curl.";
    }
}

int main() {
    std::string ip;
    std::cout << "Enter IP address: ";
    std::cin >> ip;

    std::string systemInfo = getSystemInfo(ip);
    std::cout << "System Information:\n" << systemInfo << std::endl;

    return 0;
}
