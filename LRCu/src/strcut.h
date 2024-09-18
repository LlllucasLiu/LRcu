#pragma once
#ifndef UTILS_H
#define UTILS_H

#include <chrono>
#include <thread>
#include <vector>

static void splitStr(const std::string& inputStr, const std::string& key, std::vector<std::string>& outStrVec)
{
    if (inputStr == "")
    {
        return;
    }
    int pos = inputStr.find(key);
    int oldpos = 0;
    if (pos > 0)
    {
        std::string tmp = inputStr.substr(0, pos);
        outStrVec.push_back(tmp);
    }
    while (1)
    {
        if (pos < 0)
        {
            break;
        }
        oldpos = pos;
        int newpos = inputStr.find(key, pos + key.length());
        std::string tmp = inputStr.substr(pos + key.length(), newpos - pos - key.length());
        outStrVec.push_back(tmp);
        pos = newpos;
    }
    unsigned int tmplen = 0;
    if (outStrVec.size() > 0)
    {
        tmplen = outStrVec.at(outStrVec.size() - 1).length();
    }
    if (oldpos + tmplen < inputStr.length() - 1)
    {
        std::string tmp = inputStr.substr(oldpos + key.length());
        outStrVec.push_back(tmp);
    }
}
#endif