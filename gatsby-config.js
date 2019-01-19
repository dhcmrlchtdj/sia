module.exports = {
    siteMetadata: {
        title: `H11`,
        author: `H11`,
        description: `H11's blog`,
        siteUrl: `https://blog.h11.io/`,
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
                    `gatsby-remark-breaks`,
                    `gatsby-remark-prismjs`,
                    `gatsby-remark-copy-linked-files`,
                ],
            },
        },
        {
            resolve: `gatsby-plugin-typography`,
            options: {
                pathToConfigModule: `src/utils/typography`,
            },
        },
        {
            resolve: `gatsby-plugin-google-analytics`,
            options: {
                trackingId: "UA-78944716-1",
            },
        },
        `gatsby-plugin-react-helmet`,
        `gatsby-plugin-feed`,
    ],
};
