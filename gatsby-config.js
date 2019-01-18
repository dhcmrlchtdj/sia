module.exports = {
    siteMetadata: {
        title: `Gatsby Starter Blog`,
        author: `Kyle Mathews`,
        description: `A starter blog demonstrating what Gatsby can do.`,
        siteUrl: `https://gatsby-starter-blog-demo.netlify.com/`,
        social: {
            twitter: `kylemathews`,
        },
    },
    plugins: [
        {
            resolve: `gatsby-source-filesystem`,
            options: {
                path: `${__dirname}/content`,
                name: `blog`,
            },
        },
        {
            resolve: `gatsby-transformer-remark`,
            options: {
                plugins: [
                    `gatsby-remark-prismjs`,
                    `gatsby-remark-copy-linked-files`,
                    `gatsby-remark-smartypants`,
                ],
            },
        },
        `gatsby-plugin-feed`,
        {
            resolve: `gatsby-plugin-typography`,
            options: {
                pathToConfigModule: `src/utils/typography`,
            },
        },
    ],
};
