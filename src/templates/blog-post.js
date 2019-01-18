import React from "react";
import { graphql } from "gatsby";
import Layout from "../components/Layout";
import SEO from "../components/seo";
import { rhythm, scale } from "../utils/typography";

class BlogPostTemplate extends React.Component {
    render() {
        const post = this.props.data.markdownRemark;
        const siteTitle = this.props.data.site.siteMetadata.title;

        return (
            <Layout location={this.props.location} title={siteTitle}>
                <SEO title={post.frontmatter.title} />
                <h1>{post.frontmatter.title}</h1>
                <p
                    style={{
                        ...scale(-1 / 5),
                        display: `block`,
                        marginBottom: rhythm(1),
                        marginTop: rhythm(-1),
                    }}
                >
                    {post.frontmatter.date}
                </p>
                <div dangerouslySetInnerHTML={{ __html: post.html }} />
            </Layout>
        );
    }
}

export default BlogPostTemplate;

export const pageQuery = graphql`
    query BlogPostBySlug($slug: String!) {
        site {
            siteMetadata {
                title
            }
        }
        markdownRemark(fields: { slug: { eq: $slug } }) {
            id
            html
            frontmatter {
                title
                date(formatString: "YYYY-MM-DD")
            }
        }
    }
`;
