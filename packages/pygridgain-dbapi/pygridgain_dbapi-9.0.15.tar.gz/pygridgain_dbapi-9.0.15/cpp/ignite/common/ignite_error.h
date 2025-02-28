/*
 *  Copyright (C) GridGain Systems. All Rights Reserved.
 *  _________        _____ __________________        _____
 *  __  ____/___________(_)______  /__  ____/______ ____(_)_______
 *  _  / __  __  ___/__  / _  __  / _  / __  _  __ `/__  / __  __ \
 *  / /_/ /  _  /    _  /  / /_/ /  / /_/ /  / /_/ / _  /  _  / / /
 *  \____/   /_/     /_/   \_,__/   \____/   \__,_/  /_/   /_/ /_/
 */

#pragma once

#include "error_codes.h"

#include <cstdint>
#include <exception>
#include <optional>
#include <string>
#include <any>
#include <map>

namespace ignite {

/**
 * Ignite Error.
 */
class ignite_error : public std::exception {
public:
    // Default
    ignite_error() = default;

    /**
     * Constructor.
     *
     * @param message Message.
     */
    explicit ignite_error(std::string message) noexcept
        : m_message(std::move(message)) {} // NOLINT(bugprone-throw-keyword-missing)

    /**
     * Constructor.
     *
     * @param message Message.
     */
    explicit ignite_error(std::string message, std::int32_t flags) noexcept
        : m_message(std::move(message))
        , m_flags(flags) {} // NOLINT(bugprone-throw-keyword-missing)

    /**
     * Constructor.
     *
     * @param statusCode Status code.
     * @param message Message.
     */
    explicit ignite_error(error::code code, std::string message) noexcept
        : m_status_code(code)
        , m_message(std::move(message)) {} // NOLINT(bugprone-throw-keyword-missing)

    /**
     * Constructor.
     *
     * @param statusCode Status code.
     * @param message Message.
     * @param cause Error cause.
     */
    explicit ignite_error(error::code code, std::string message, std::exception_ptr cause) noexcept
        : m_status_code(code)
        , m_message(std::move(message))
        , m_cause(std::move(cause)) {} // NOLINT(bugprone-throw-keyword-missing)

    /**
     * Get error message.
     */
    [[nodiscard]] char const *what() const noexcept override { return m_message.c_str(); }

    /**
     * Get error message as std::string.
     */
    [[nodiscard]] const std::string &what_str() const noexcept { return m_message; }

    /**
     * Get status code.
     *
     * @return Status code.
     */
    [[nodiscard]] error::code get_status_code() const noexcept { return m_status_code; }

    /**
     * Get error cause.
     *
     * @return Error cause. Can be empty.
     */
    [[nodiscard]] std::exception_ptr get_cause() const noexcept { return m_cause; }

    /**
     * Get flags.
     * Internal method.
     *
     * @return Flags.
     */
    [[nodiscard]] std::int32_t get_flags() const noexcept { return m_flags; }

    /**
     * Add an extra information.
     *
     * @tparam T Extra type.
     * @param key Key.
     * @param value value.
     */
    template<typename T>
    void add_extra(std::string key, T value) {
        m_extras.emplace(std::pair{std::move(key), std::any{std::move(value)}});
    }

    /**
     * Get an extra information by the key.
     *
     * @return Extra.
     */
    template<typename T>
    [[nodiscard]] std::optional<T> get_extra(const std::string &key) const noexcept {
        auto it = m_extras.find(key);
        if (it == m_extras.end())
            return {};

        return std::any_cast<T>(it->second);
    }

private:
    /** Status code. */
    error::code m_status_code{error::code::INTERNAL};

    /** Message. */
    std::string m_message;

    /** Cause. */
    std::exception_ptr m_cause;

    /** Flags. */
    std::int32_t m_flags{0};

    /** Extras. */
    std::map<std::string, std::any> m_extras;
};

} // namespace ignite
