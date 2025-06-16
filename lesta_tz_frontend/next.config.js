/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    output: 'standalone',
    compiler: {
        styledComponents: true,
    },
    i18n: {
        locales: ['ru', 'en'],
        defaultLocale: 'ru',
        localeDetection: false,
    },
    publicRuntimeConfig: {
        NEXT_PUBLIC_DOMAIN: process.env.NEXT_PUBLIC_DOMAIN
    },
    
    eslint: {
        ignoreDuringBuilds: true,
    },
}



module.exports = nextConfig
