import React from "react";
import { Link, graphql } from "gatsby";
import Layout from "../components/Layout";
import SEO from "../components/seo";
import CC from "../components/cc";

class BlogIndex extends React.Component {
    render() {
        const { data } = this.props;
        const siteTitle = data.site.siteMetadata.title;
        const posts = data.allMarkdownRemark.edges;

        return (
            <Layout location={this.props.location} title={siteTitle}>
                <SEO title="All posts" />
                {posts.map(({ node }) => {
                    const title = node.frontmatter.title || node.fields.slug;
                    return (
                        <div key={node.fields.slug}>
                            <h3 style={{ marginBottom: 0 }}>
                                <Link to={node.fields.slug}>{title}</Link>
                            </h3>
                            <small>{node.frontmatter.date}</small>
                        </div>
                    );
                })}
                <CC />
            </Layout>
        );
    }
}

export default BlogIndex;

export const pageQuery = graphql`
    query {
        site {
            siteMetadata {
                title
            }
        }
        allMarkdownRemark(sort: { fields: [frontmatter___date], order: DESC }) {
            edges {
                node {
                    fields {
                        slug
                    }
                    frontmatter {
                        date(formatString: "YYYY-MM-DD")
                        title
                    }
                }
            }
        }
    }
`;
