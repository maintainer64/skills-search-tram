/** @type {import('next-sitemap').IConfig} */
module.exports = {
    siteUrl: process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : 'https://arrive.gubanov.site',
    generateRobotsTxt: true,
    trailingSlash: true,
    targetDirectory: `${__dirname}/public`,
    // Wherever are your pages stored
    pagesDirectory: `${__dirname}/src/pages`,
};
