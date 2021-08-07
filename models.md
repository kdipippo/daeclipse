# All Dependencies
```mermaid
graph LR
    Collection --> CollectionInfo
    Collection --> Deviation
    Collection --> Gruser
    CollectionInfo --> Deviation
    CollectionInfo --> Gruser
    Comment --> CommentContent
    Comment --> Gruser
    CommentsList --> Comment
    Deviation --> DeviationExtendedContent
    Deviation --> DeviationMedia
    Deviation --> Stats
    DeviationExtendedResult --> CommentsList
    DeviationExtendedResult --> Deviation
    DeviationExtendedContent --> DeviationAwardedBadge
    DeviationExtendedContent --> DeviationExtendedStats
    DeviationExtendedContent --> DeviationFileSpecs
    DeviationExtendedContent --> DeviationRelatedStreams
    DeviationExtendedContent --> DeviationTypeFacet
    DeviationRelatedStreams --> Collection
    DeviationRelatedStreams --> Deviation
    Folder --> Deviation
    Folder --> Gruser
    GroupsList --> Gruser
```
