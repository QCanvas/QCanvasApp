import sgqlc.types
import sgqlc.types.datetime
import sgqlc.types.relay


canvas_schema = sgqlc.types.Schema()


# Unexport Node/PageInfo, let schema re-declare them
canvas_schema -= sgqlc.types.relay.Node
canvas_schema -= sgqlc.types.relay.PageInfo



########################################################################
# Scalars and Enumerations
########################################################################
class AssessmentType(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('grading', 'peer_review', 'provisional_grade')


class AssignmentGroupState(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('available', 'deleted')


class AssignmentState(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('deleted', 'duplicating', 'fail_to_import', 'failed_to_duplicate', 'failed_to_migrate', 'importing', 'migrating', 'published', 'unpublished')


class AutoLeaderPolicy(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('first', 'random')


Boolean = sgqlc.types.Boolean

class CourseFilterableEnrollmentState(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('active', 'completed', 'creation_pending', 'inactive', 'invited', 'rejected')


class CourseFilterableEnrollmentType(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('DesignerEnrollment', 'ObserverEnrollment', 'StudentEnrollment', 'StudentViewEnrollment', 'TaEnrollment', 'TeacherEnrollment')


class CourseWorkflowState(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('available', 'claimed', 'completed', 'created', 'deleted')


DateTime = sgqlc.types.datetime.DateTime

class DiscussionFilterType(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('all', 'deleted', 'drafts', 'unread')


class DiscussionSortOrderType(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('asc', 'desc')


class DraftableSubmissionType(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('basic_lti_launch', 'media_recording', 'online_text_entry', 'online_upload', 'online_url', 'student_annotation')


class EnrollmentType(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('DesignerEnrollment', 'ObserverEnrollment', 'StudentEnrollment', 'StudentViewEnrollment', 'TaEnrollment', 'TeacherEnrollment')


class EnrollmentWorkflowState(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('active', 'completed', 'creation_pending', 'deleted', 'inactive', 'invited', 'rejected')


class ExternalToolPlacement(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('homework_submission',)


class ExternalToolState(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('anonymous', 'email_only', 'name_only', 'public')


Float = sgqlc.types.Float

class GradeState(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('active', 'deleted')


class GradingType(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('gpa_scale', 'letter_grade', 'not_graded', 'pass_fail', 'percent', 'points')


class GroupMembershipState(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('accepted', 'deleted', 'invited', 'rejected', 'requested')


ID = sgqlc.types.ID

class ISO8601DateTime(sgqlc.types.Scalar):
    __schema__ = canvas_schema


Int = sgqlc.types.Int

class JSON(sgqlc.types.Scalar):
    __schema__ = canvas_schema


class LatePolicyStatusType(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('extended', 'late', 'missing', 'none')


class MediaType(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('audio', 'video')


class NodeType(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('Account', 'Assignment', 'AssignmentGroup', 'Conversation', 'Course', 'Discussion', 'DiscussionEntry', 'Enrollment', 'File', 'GradingPeriod', 'GradingPeriodGroup', 'Group', 'GroupSet', 'InternalSetting', 'LearningOutcomeGroup', 'MediaObject', 'Module', 'ModuleItem', 'OutcomeCalculationMethod', 'OutcomeProficiency', 'Page', 'PostPolicy', 'Progress', 'Rubric', 'Section', 'Submission', 'Term', 'UsageRights', 'User')


class NotificationCategoryType(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('Account_Notification', 'Added_To_Conversation', 'All_Submissions', 'Announcement', 'Announcement_Created_By_You', 'Appointment_Availability', 'Appointment_Cancelations', 'Appointment_Signups', 'Blueprint', 'Calendar', 'Content_Link_Error', 'Conversation_Created', 'Conversation_Message', 'Course_Content', 'Discussion', 'DiscussionEntry', 'DiscussionMention', 'Due_Date', 'Files', 'Grading', 'Grading_Policies', 'Invitation', 'Late_Grading', 'Membership_Update', 'Other', 'Recording_Ready', 'ReportedReply', 'Student_Appointment_Signups', 'Submission_Comment')


class NotificationFrequencyType(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('daily', 'immediately', 'never', 'weekly')


class NotificationPreferencesContextType(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('Account', 'Course')


class OnlineSubmissionType(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('basic_lti_launch', 'media_recording', 'online_text_entry', 'online_upload', 'online_url', 'student_annotation')


class OrderDirection(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('ascending', 'descending')


class ProgressState(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('completed', 'failed', 'queued', 'running')


class RatingInputType(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('liked', 'not_liked')


class ReportType(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('inappropriate', 'offensive', 'other')


class SelfSignupPolicy(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('disabled', 'enabled', 'restricted')


String = sgqlc.types.String

class SubmissionCommentsSortOrderType(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('asc', 'desc')


class SubmissionGradingStatus(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('excused', 'graded', 'needs_grading', 'needs_review')


class SubmissionOrderField(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('_id', 'gradedAt')


class SubmissionSearchOrderField(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('score', 'submitted_at', 'username')


class SubmissionState(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('deleted', 'graded', 'pending_review', 'submitted', 'ungraded', 'unsubmitted')


class SubmissionType(sgqlc.types.Enum):
    __schema__ = canvas_schema
    __choices__ = ('attendance', 'basic_lti_launch', 'discussion_topic', 'external_tool', 'media_recording', 'none', 'not_graded', 'on_paper', 'online_quiz', 'online_text_entry', 'online_upload', 'online_url', 'student_annotation', 'wiki_page')


class URL(sgqlc.types.Scalar):
    __schema__ = canvas_schema



########################################################################
# Input Objects
########################################################################
class AddConversationMessageInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('conversation_id', 'body', 'recipients', 'included_messages', 'attachment_ids', 'media_comment_id', 'media_comment_type', 'context_code', 'user_note')
    conversation_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='conversationId')
    body = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='body')
    recipients = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='recipients')
    included_messages = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='includedMessages')
    attachment_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='attachmentIds')
    media_comment_id = sgqlc.types.Field(ID, graphql_name='mediaCommentId')
    media_comment_type = sgqlc.types.Field(String, graphql_name='mediaCommentType')
    context_code = sgqlc.types.Field(String, graphql_name='contextCode')
    user_note = sgqlc.types.Field(Boolean, graphql_name='userNote')


class AssignmentCreate(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('assignment_group_id', 'assignment_overrides', 'due_at', 'grading_type', 'grading_standard_id', 'group_category_id', 'lock_at', 'peer_reviews', 'points_possible', 'unlock_at', 'post_to_sis', 'only_visible_to_overrides', 'course_id', 'name')
    assignment_group_id = sgqlc.types.Field(ID, graphql_name='assignmentGroupId')
    assignment_overrides = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('AssignmentOverrideCreateOrUpdate')), graphql_name='assignmentOverrides')
    due_at = sgqlc.types.Field(DateTime, graphql_name='dueAt')
    grading_type = sgqlc.types.Field(GradingType, graphql_name='gradingType')
    grading_standard_id = sgqlc.types.Field(ID, graphql_name='gradingStandardId')
    group_category_id = sgqlc.types.Field(ID, graphql_name='groupCategoryId')
    lock_at = sgqlc.types.Field(DateTime, graphql_name='lockAt')
    peer_reviews = sgqlc.types.Field('AssignmentPeerReviewsUpdate', graphql_name='peerReviews')
    points_possible = sgqlc.types.Field(Float, graphql_name='pointsPossible')
    unlock_at = sgqlc.types.Field(DateTime, graphql_name='unlockAt')
    post_to_sis = sgqlc.types.Field(Boolean, graphql_name='postToSis')
    only_visible_to_overrides = sgqlc.types.Field(Boolean, graphql_name='onlyVisibleToOverrides')
    course_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='courseId')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')


class AssignmentFilter(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('user_id', 'grading_period_id')
    user_id = sgqlc.types.Field(ID, graphql_name='userId')
    grading_period_id = sgqlc.types.Field(ID, graphql_name='gradingPeriodId')


class AssignmentModeratedGradingUpdate(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('enabled', 'grader_count', 'grader_comments_visible_to_graders', 'grader_names_visible_to_final_grader', 'graders_anonymous_to_graders', 'final_grader_id')
    enabled = sgqlc.types.Field(Boolean, graphql_name='enabled')
    grader_count = sgqlc.types.Field(Int, graphql_name='graderCount')
    grader_comments_visible_to_graders = sgqlc.types.Field(Boolean, graphql_name='graderCommentsVisibleToGraders')
    grader_names_visible_to_final_grader = sgqlc.types.Field(Boolean, graphql_name='graderNamesVisibleToFinalGrader')
    graders_anonymous_to_graders = sgqlc.types.Field(Boolean, graphql_name='gradersAnonymousToGraders')
    final_grader_id = sgqlc.types.Field(ID, graphql_name='finalGraderId')


class AssignmentOverrideCreateOrUpdate(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('id', 'due_at', 'lock_at', 'unlock_at', 'course_section_id', 'group_id', 'student_ids', 'noop_id', 'title')
    id = sgqlc.types.Field(ID, graphql_name='id')
    due_at = sgqlc.types.Field(DateTime, graphql_name='dueAt')
    lock_at = sgqlc.types.Field(DateTime, graphql_name='lockAt')
    unlock_at = sgqlc.types.Field(DateTime, graphql_name='unlockAt')
    course_section_id = sgqlc.types.Field(ID, graphql_name='courseSectionId')
    group_id = sgqlc.types.Field(ID, graphql_name='groupId')
    student_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='studentIds')
    noop_id = sgqlc.types.Field(ID, graphql_name='noopId')
    title = sgqlc.types.Field(String, graphql_name='title')


class AssignmentPeerReviewsUpdate(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('enabled', 'count', 'due_at', 'intra_reviews', 'anonymous_reviews', 'automatic_reviews')
    enabled = sgqlc.types.Field(Boolean, graphql_name='enabled')
    count = sgqlc.types.Field(Int, graphql_name='count')
    due_at = sgqlc.types.Field(DateTime, graphql_name='dueAt')
    intra_reviews = sgqlc.types.Field(Boolean, graphql_name='intraReviews')
    anonymous_reviews = sgqlc.types.Field(Boolean, graphql_name='anonymousReviews')
    automatic_reviews = sgqlc.types.Field(Boolean, graphql_name='automaticReviews')


class AssignmentUpdate(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('assignment_group_id', 'assignment_overrides', 'due_at', 'grading_type', 'grading_standard_id', 'group_category_id', 'lock_at', 'peer_reviews', 'points_possible', 'unlock_at', 'post_to_sis', 'only_visible_to_overrides', 'set_assignment')
    assignment_group_id = sgqlc.types.Field(ID, graphql_name='assignmentGroupId')
    assignment_overrides = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(AssignmentOverrideCreateOrUpdate)), graphql_name='assignmentOverrides')
    due_at = sgqlc.types.Field(DateTime, graphql_name='dueAt')
    grading_type = sgqlc.types.Field(GradingType, graphql_name='gradingType')
    grading_standard_id = sgqlc.types.Field(ID, graphql_name='gradingStandardId')
    group_category_id = sgqlc.types.Field(ID, graphql_name='groupCategoryId')
    lock_at = sgqlc.types.Field(DateTime, graphql_name='lockAt')
    peer_reviews = sgqlc.types.Field(AssignmentPeerReviewsUpdate, graphql_name='peerReviews')
    points_possible = sgqlc.types.Field(Float, graphql_name='pointsPossible')
    unlock_at = sgqlc.types.Field(DateTime, graphql_name='unlockAt')
    post_to_sis = sgqlc.types.Field(Boolean, graphql_name='postToSis')
    only_visible_to_overrides = sgqlc.types.Field(Boolean, graphql_name='onlyVisibleToOverrides')
    set_assignment = sgqlc.types.Field(Boolean, graphql_name='setAssignment')


class CourseUsersFilter(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('user_ids', 'enrollment_states', 'enrollment_types')
    user_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='userIds')
    enrollment_states = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(CourseFilterableEnrollmentState)), graphql_name='enrollmentStates')
    enrollment_types = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(CourseFilterableEnrollmentType)), graphql_name='enrollmentTypes')


class CreateAccountDomainLookupInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('account_domain_id', 'authentication_provider', 'name')
    account_domain_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='accountDomainId')
    authentication_provider = sgqlc.types.Field(String, graphql_name='authenticationProvider')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')


class CreateAssignmentInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('state', 'due_at', 'lock_at', 'unlock_at', 'description', 'assignment_overrides', 'position', 'points_possible', 'grading_type', 'allowed_extensions', 'assignment_group_id', 'group_set_id', 'allowed_attempts', 'only_visible_to_overrides', 'submission_types', 'grading_standard_id', 'peer_reviews', 'moderated_grading', 'grade_group_students_individually', 'group_category_id', 'omit_from_final_grade', 'anonymous_instructor_annotations', 'post_to_sis', 'anonymous_grading', 'module_ids', 'course_id', 'name')
    state = sgqlc.types.Field(AssignmentState, graphql_name='state')
    due_at = sgqlc.types.Field(DateTime, graphql_name='dueAt')
    lock_at = sgqlc.types.Field(DateTime, graphql_name='lockAt')
    unlock_at = sgqlc.types.Field(DateTime, graphql_name='unlockAt')
    description = sgqlc.types.Field(String, graphql_name='description')
    assignment_overrides = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(AssignmentOverrideCreateOrUpdate)), graphql_name='assignmentOverrides')
    position = sgqlc.types.Field(Int, graphql_name='position')
    points_possible = sgqlc.types.Field(Float, graphql_name='pointsPossible')
    grading_type = sgqlc.types.Field(GradingType, graphql_name='gradingType')
    allowed_extensions = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='allowedExtensions')
    assignment_group_id = sgqlc.types.Field(ID, graphql_name='assignmentGroupId')
    group_set_id = sgqlc.types.Field(ID, graphql_name='groupSetId')
    allowed_attempts = sgqlc.types.Field(Int, graphql_name='allowedAttempts')
    only_visible_to_overrides = sgqlc.types.Field(Boolean, graphql_name='onlyVisibleToOverrides')
    submission_types = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(SubmissionType)), graphql_name='submissionTypes')
    grading_standard_id = sgqlc.types.Field(ID, graphql_name='gradingStandardId')
    peer_reviews = sgqlc.types.Field(AssignmentPeerReviewsUpdate, graphql_name='peerReviews')
    moderated_grading = sgqlc.types.Field(AssignmentModeratedGradingUpdate, graphql_name='moderatedGrading')
    grade_group_students_individually = sgqlc.types.Field(Boolean, graphql_name='gradeGroupStudentsIndividually')
    group_category_id = sgqlc.types.Field(ID, graphql_name='groupCategoryId')
    omit_from_final_grade = sgqlc.types.Field(Boolean, graphql_name='omitFromFinalGrade')
    anonymous_instructor_annotations = sgqlc.types.Field(Boolean, graphql_name='anonymousInstructorAnnotations')
    post_to_sis = sgqlc.types.Field(Boolean, graphql_name='postToSis')
    anonymous_grading = sgqlc.types.Field(Boolean, graphql_name='anonymousGrading')
    module_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='moduleIds')
    course_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='courseId')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')


class CreateCommentBankItemInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('course_id', 'comment')
    course_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='courseId')
    comment = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='comment')


class CreateConversationInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('recipients', 'subject', 'body', 'bulk_message', 'force_new', 'group_conversation', 'attachment_ids', 'media_comment_id', 'media_comment_type', 'context_code', 'conversation_id', 'user_note', 'tags')
    recipients = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='recipients')
    subject = sgqlc.types.Field(String, graphql_name='subject')
    body = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='body')
    bulk_message = sgqlc.types.Field(Boolean, graphql_name='bulkMessage')
    force_new = sgqlc.types.Field(Boolean, graphql_name='forceNew')
    group_conversation = sgqlc.types.Field(Boolean, graphql_name='groupConversation')
    attachment_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='attachmentIds')
    media_comment_id = sgqlc.types.Field(ID, graphql_name='mediaCommentId')
    media_comment_type = sgqlc.types.Field(String, graphql_name='mediaCommentType')
    context_code = sgqlc.types.Field(String, graphql_name='contextCode')
    conversation_id = sgqlc.types.Field(ID, graphql_name='conversationId')
    user_note = sgqlc.types.Field(Boolean, graphql_name='userNote')
    tags = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='tags')


class CreateDiscussionEntryDraftInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('discussion_topic_id', 'discussion_entry_id', 'parent_id', 'file_id', 'message')
    discussion_topic_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='discussionTopicId')
    discussion_entry_id = sgqlc.types.Field(ID, graphql_name='discussionEntryId')
    parent_id = sgqlc.types.Field(ID, graphql_name='parentId')
    file_id = sgqlc.types.Field(ID, graphql_name='fileId')
    message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='message')


class CreateDiscussionEntryInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('discussion_topic_id', 'message', 'parent_entry_id', 'file_id', 'is_anonymous_author', 'quoted_entry_id')
    discussion_topic_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='discussionTopicId')
    message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='message')
    parent_entry_id = sgqlc.types.Field(ID, graphql_name='parentEntryId')
    file_id = sgqlc.types.Field(ID, graphql_name='fileId')
    is_anonymous_author = sgqlc.types.Field(Boolean, graphql_name='isAnonymousAuthor')
    quoted_entry_id = sgqlc.types.Field(ID, graphql_name='quotedEntryId')


class CreateDiscussionTopicInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('allow_rating', 'delayed_post_at', 'group_category_id', 'lock_at', 'locked', 'message', 'only_graders_can_rate', 'published', 'require_initial_post', 'title', 'todo_date', 'podcast_enabled', 'podcast_has_student_posts', 'specific_sections', 'file_id', 'is_announcement', 'is_anonymous_author', 'anonymous_state', 'context_id', 'context_type', 'assignment')
    allow_rating = sgqlc.types.Field(Boolean, graphql_name='allowRating')
    delayed_post_at = sgqlc.types.Field(DateTime, graphql_name='delayedPostAt')
    group_category_id = sgqlc.types.Field(ID, graphql_name='groupCategoryId')
    lock_at = sgqlc.types.Field(DateTime, graphql_name='lockAt')
    locked = sgqlc.types.Field(Boolean, graphql_name='locked')
    message = sgqlc.types.Field(String, graphql_name='message')
    only_graders_can_rate = sgqlc.types.Field(Boolean, graphql_name='onlyGradersCanRate')
    published = sgqlc.types.Field(Boolean, graphql_name='published')
    require_initial_post = sgqlc.types.Field(Boolean, graphql_name='requireInitialPost')
    title = sgqlc.types.Field(String, graphql_name='title')
    todo_date = sgqlc.types.Field(DateTime, graphql_name='todoDate')
    podcast_enabled = sgqlc.types.Field(Boolean, graphql_name='podcastEnabled')
    podcast_has_student_posts = sgqlc.types.Field(Boolean, graphql_name='podcastHasStudentPosts')
    specific_sections = sgqlc.types.Field(String, graphql_name='specificSections')
    file_id = sgqlc.types.Field(ID, graphql_name='fileId')
    is_announcement = sgqlc.types.Field(Boolean, graphql_name='isAnnouncement')
    is_anonymous_author = sgqlc.types.Field(Boolean, graphql_name='isAnonymousAuthor')
    anonymous_state = sgqlc.types.Field(String, graphql_name='anonymousState')
    context_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contextId')
    context_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='contextType')
    assignment = sgqlc.types.Field(AssignmentCreate, graphql_name='assignment')


class CreateGroupInSetInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('name', 'group_set_id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    group_set_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='groupSetId')


class CreateInternalSettingInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('name', 'value')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='value')


class CreateLearningOutcomeGroupInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('id', 'title', 'description', 'vendor_guid')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    description = sgqlc.types.Field(String, graphql_name='description')
    vendor_guid = sgqlc.types.Field(String, graphql_name='vendorGuid')


class CreateLearningOutcomeInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('title', 'description', 'display_name', 'vendor_guid', 'calculation_method', 'calculation_int', 'mastery_points', 'ratings', 'group_id')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    description = sgqlc.types.Field(String, graphql_name='description')
    display_name = sgqlc.types.Field(String, graphql_name='displayName')
    vendor_guid = sgqlc.types.Field(String, graphql_name='vendorGuid')
    calculation_method = sgqlc.types.Field(String, graphql_name='calculationMethod')
    calculation_int = sgqlc.types.Field(Int, graphql_name='calculationInt')
    mastery_points = sgqlc.types.Field(Float, graphql_name='masteryPoints')
    ratings = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ProficiencyRatingInput')), graphql_name='ratings')
    group_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='groupId')


class CreateModuleInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('name', 'course_id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    course_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='courseId')


class CreateOutcomeCalculationMethodInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('context_type', 'context_id', 'calculation_method', 'calculation_int')
    context_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='contextType')
    context_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contextId')
    calculation_method = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='calculationMethod')
    calculation_int = sgqlc.types.Field(Int, graphql_name='calculationInt')


class CreateOutcomeProficiencyInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('context_type', 'context_id', 'proficiency_ratings')
    context_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='contextType')
    context_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contextId')
    proficiency_ratings = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('OutcomeProficiencyRatingCreate'))), graphql_name='proficiencyRatings')


class CreateSubmissionCommentInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('submission_id', 'attempt', 'comment', 'file_ids', 'media_object_id', 'media_object_type', 'reviewer_submission_id')
    submission_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='submissionId')
    attempt = sgqlc.types.Field(Int, graphql_name='attempt')
    comment = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='comment')
    file_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='fileIds')
    media_object_id = sgqlc.types.Field(ID, graphql_name='mediaObjectId')
    media_object_type = sgqlc.types.Field(String, graphql_name='mediaObjectType')
    reviewer_submission_id = sgqlc.types.Field(ID, graphql_name='reviewerSubmissionId')


class CreateSubmissionDraftInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('active_submission_type', 'attempt', 'body', 'external_tool_id', 'file_ids', 'lti_launch_url', 'media_id', 'resource_link_lookup_uuid', 'submission_id', 'url')
    active_submission_type = sgqlc.types.Field(sgqlc.types.non_null(DraftableSubmissionType), graphql_name='activeSubmissionType')
    attempt = sgqlc.types.Field(Int, graphql_name='attempt')
    body = sgqlc.types.Field(String, graphql_name='body')
    external_tool_id = sgqlc.types.Field(ID, graphql_name='externalToolId')
    file_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='fileIds')
    lti_launch_url = sgqlc.types.Field(String, graphql_name='ltiLaunchUrl')
    media_id = sgqlc.types.Field(ID, graphql_name='mediaId')
    resource_link_lookup_uuid = sgqlc.types.Field(String, graphql_name='resourceLinkLookupUuid')
    submission_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='submissionId')
    url = sgqlc.types.Field(String, graphql_name='url')


class CreateSubmissionInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('annotatable_attachment_id', 'assignment_id', 'body', 'file_ids', 'media_id', 'resource_link_lookup_uuid', 'submission_type', 'url', 'student_id')
    annotatable_attachment_id = sgqlc.types.Field(ID, graphql_name='annotatableAttachmentId')
    assignment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assignmentId')
    body = sgqlc.types.Field(String, graphql_name='body')
    file_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='fileIds')
    media_id = sgqlc.types.Field(ID, graphql_name='mediaId')
    resource_link_lookup_uuid = sgqlc.types.Field(String, graphql_name='resourceLinkLookupUuid')
    submission_type = sgqlc.types.Field(sgqlc.types.non_null(OnlineSubmissionType), graphql_name='submissionType')
    url = sgqlc.types.Field(String, graphql_name='url')
    student_id = sgqlc.types.Field(ID, graphql_name='studentId')


class CreateUserInboxLabelInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('names',)
    names = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='names')


class DeleteAccountDomainLookupInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')


class DeleteCommentBankItemInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')


class DeleteConversationMessagesInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('ids',)
    ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids')


class DeleteConversationsInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('ids',)
    ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids')


class DeleteCustomGradeStatusInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')


class DeleteDiscussionEntryInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')


class DeleteDiscussionTopicInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')


class DeleteInternalSettingInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('internal_setting_id',)
    internal_setting_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='internalSettingId')


class DeleteOutcomeCalculationMethodInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')


class DeleteOutcomeLinksInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('ids',)
    ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids')


class DeleteOutcomeProficiencyInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')


class DeleteSubmissionDraftInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('submission_id',)
    submission_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='submissionId')


class DeleteUserInboxLabelInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('names',)
    names = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='names')


class EnrollmentFilterInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('types', 'associated_user_ids', 'states')
    types = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(EnrollmentType)), graphql_name='types')
    associated_user_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='associatedUserIds')
    states = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(EnrollmentWorkflowState)), graphql_name='states')


class ExternalToolFilterInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('state', 'placement')
    state = sgqlc.types.Field(ExternalToolState, graphql_name='state')
    placement = sgqlc.types.Field(ExternalToolPlacement, graphql_name='placement')


class GradesEnrollmentFilter(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('enrollment_ids',)
    enrollment_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='enrollmentIds')


class HideAssignmentGradesForSectionsInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('assignment_id', 'section_ids')
    assignment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assignmentId')
    section_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='sectionIds')


class HideAssignmentGradesInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('assignment_id', 'section_ids', 'only_student_ids', 'skip_student_ids')
    assignment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assignmentId')
    section_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='sectionIds')
    only_student_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='onlyStudentIds')
    skip_student_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='skipStudentIds')


class ImportOutcomesInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('group_id', 'outcome_id', 'source_context_id', 'source_context_type', 'target_group_id', 'target_context_id', 'target_context_type')
    group_id = sgqlc.types.Field(ID, graphql_name='groupId')
    outcome_id = sgqlc.types.Field(ID, graphql_name='outcomeId')
    source_context_id = sgqlc.types.Field(ID, graphql_name='sourceContextId')
    source_context_type = sgqlc.types.Field(String, graphql_name='sourceContextType')
    target_group_id = sgqlc.types.Field(ID, graphql_name='targetGroupId')
    target_context_id = sgqlc.types.Field(ID, graphql_name='targetContextId')
    target_context_type = sgqlc.types.Field(String, graphql_name='targetContextType')


class MarkSubmissionCommentsReadInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('submission_comment_ids', 'submission_id')
    submission_comment_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='submissionCommentIds')
    submission_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='submissionId')


class MoveOutcomeLinksInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('outcome_link_ids', 'group_id')
    outcome_link_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='outcomeLinkIds')
    group_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='groupId')


class OutcomeProficiencyRatingCreate(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('color', 'description', 'mastery', 'points')
    color = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='color')
    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')
    mastery = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='mastery')
    points = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='points')


class PostAssignmentGradesForSectionsInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('assignment_id', 'section_ids', 'graded_only')
    assignment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assignmentId')
    section_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='sectionIds')
    graded_only = sgqlc.types.Field(Boolean, graphql_name='gradedOnly')


class PostAssignmentGradesInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('assignment_id', 'section_ids', 'only_student_ids', 'skip_student_ids', 'graded_only')
    assignment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assignmentId')
    section_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='sectionIds')
    only_student_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='onlyStudentIds')
    skip_student_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='skipStudentIds')
    graded_only = sgqlc.types.Field(Boolean, graphql_name='gradedOnly')


class ProficiencyRatingInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('description', 'points')
    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')
    points = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='points')


class SetAssignmentPostPolicyInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('assignment_id', 'post_manually')
    assignment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assignmentId')
    post_manually = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='postManually')


class SetCoursePostPolicyInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('course_id', 'post_manually')
    course_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='courseId')
    post_manually = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='postManually')


class SetFriendlyDescriptionInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('description', 'outcome_id', 'context_id', 'context_type')
    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')
    outcome_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='outcomeId')
    context_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contextId')
    context_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='contextType')


class SetModuleItemCompletionInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('module_id', 'item_id', 'done')
    module_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='moduleId')
    item_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='itemId')
    done = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='done')


class SetOverrideScoreInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('enrollment_id', 'grading_period_id', 'override_score')
    enrollment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='enrollmentId')
    grading_period_id = sgqlc.types.Field(ID, graphql_name='gradingPeriodId')
    override_score = sgqlc.types.Field(Float, graphql_name='overrideScore')


class SetOverrideStatusInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('custom_grade_status_id', 'enrollment_id', 'grading_period_id')
    custom_grade_status_id = sgqlc.types.Field(ID, graphql_name='customGradeStatusId')
    enrollment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='enrollmentId')
    grading_period_id = sgqlc.types.Field(ID, graphql_name='gradingPeriodId')


class SubmissionCommentFilterInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('all_comments', 'for_attempt', 'peer_review')
    all_comments = sgqlc.types.Field(Boolean, graphql_name='allComments')
    for_attempt = sgqlc.types.Field(Int, graphql_name='forAttempt')
    peer_review = sgqlc.types.Field(Boolean, graphql_name='peerReview')


class SubmissionFilterInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('states', 'section_ids', 'submitted_since', 'graded_since', 'updated_since')
    states = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(SubmissionState)), graphql_name='states')
    section_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='sectionIds')
    submitted_since = sgqlc.types.Field(DateTime, graphql_name='submittedSince')
    graded_since = sgqlc.types.Field(DateTime, graphql_name='gradedSince')
    updated_since = sgqlc.types.Field(DateTime, graphql_name='updatedSince')


class SubmissionHistoryFilterInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('states', 'include_current_submission')
    states = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(SubmissionState)), graphql_name='states')
    include_current_submission = sgqlc.types.Field(Boolean, graphql_name='includeCurrentSubmission')


class SubmissionOrderCriteria(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('field', 'direction')
    field = sgqlc.types.Field(sgqlc.types.non_null(SubmissionOrderField), graphql_name='field')
    direction = sgqlc.types.Field(OrderDirection, graphql_name='direction')


class SubmissionRubricAssessmentFilterInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('for_attempt',)
    for_attempt = sgqlc.types.Field(Int, graphql_name='forAttempt')


class SubmissionSearchFilterInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('include_unsubmitted', 'states', 'section_ids', 'enrollment_types', 'user_search', 'user_id', 'scored_less_than', 'scored_more_than', 'late', 'grading_status')
    include_unsubmitted = sgqlc.types.Field(Boolean, graphql_name='includeUnsubmitted')
    states = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(SubmissionState)), graphql_name='states')
    section_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='sectionIds')
    enrollment_types = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(EnrollmentType)), graphql_name='enrollmentTypes')
    user_search = sgqlc.types.Field(String, graphql_name='userSearch')
    user_id = sgqlc.types.Field(ID, graphql_name='userId')
    scored_less_than = sgqlc.types.Field(Float, graphql_name='scoredLessThan')
    scored_more_than = sgqlc.types.Field(Float, graphql_name='scoredMoreThan')
    late = sgqlc.types.Field(Boolean, graphql_name='late')
    grading_status = sgqlc.types.Field(SubmissionGradingStatus, graphql_name='gradingStatus')


class SubmissionSearchOrder(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('field', 'direction')
    field = sgqlc.types.Field(sgqlc.types.non_null(SubmissionSearchOrderField), graphql_name='field')
    direction = sgqlc.types.Field(OrderDirection, graphql_name='direction')


class SubscribeToDiscussionTopicInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('discussion_topic_id', 'subscribed')
    discussion_topic_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='discussionTopicId')
    subscribed = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='subscribed')


class UpdateAccountDomainLookupInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('account_domain_id', 'account_domain_lookup_id', 'authentication_provider', 'name')
    account_domain_id = sgqlc.types.Field(ID, graphql_name='accountDomainId')
    account_domain_lookup_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='accountDomainLookupId')
    authentication_provider = sgqlc.types.Field(String, graphql_name='authenticationProvider')
    name = sgqlc.types.Field(String, graphql_name='name')


class UpdateAssignmentInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('state', 'due_at', 'lock_at', 'unlock_at', 'description', 'assignment_overrides', 'position', 'points_possible', 'grading_type', 'allowed_extensions', 'assignment_group_id', 'group_set_id', 'allowed_attempts', 'only_visible_to_overrides', 'submission_types', 'grading_standard_id', 'peer_reviews', 'moderated_grading', 'grade_group_students_individually', 'group_category_id', 'omit_from_final_grade', 'anonymous_instructor_annotations', 'post_to_sis', 'anonymous_grading', 'module_ids', 'id', 'name')
    state = sgqlc.types.Field(AssignmentState, graphql_name='state')
    due_at = sgqlc.types.Field(DateTime, graphql_name='dueAt')
    lock_at = sgqlc.types.Field(DateTime, graphql_name='lockAt')
    unlock_at = sgqlc.types.Field(DateTime, graphql_name='unlockAt')
    description = sgqlc.types.Field(String, graphql_name='description')
    assignment_overrides = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(AssignmentOverrideCreateOrUpdate)), graphql_name='assignmentOverrides')
    position = sgqlc.types.Field(Int, graphql_name='position')
    points_possible = sgqlc.types.Field(Float, graphql_name='pointsPossible')
    grading_type = sgqlc.types.Field(GradingType, graphql_name='gradingType')
    allowed_extensions = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='allowedExtensions')
    assignment_group_id = sgqlc.types.Field(ID, graphql_name='assignmentGroupId')
    group_set_id = sgqlc.types.Field(ID, graphql_name='groupSetId')
    allowed_attempts = sgqlc.types.Field(Int, graphql_name='allowedAttempts')
    only_visible_to_overrides = sgqlc.types.Field(Boolean, graphql_name='onlyVisibleToOverrides')
    submission_types = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(SubmissionType)), graphql_name='submissionTypes')
    grading_standard_id = sgqlc.types.Field(ID, graphql_name='gradingStandardId')
    peer_reviews = sgqlc.types.Field(AssignmentPeerReviewsUpdate, graphql_name='peerReviews')
    moderated_grading = sgqlc.types.Field(AssignmentModeratedGradingUpdate, graphql_name='moderatedGrading')
    grade_group_students_individually = sgqlc.types.Field(Boolean, graphql_name='gradeGroupStudentsIndividually')
    group_category_id = sgqlc.types.Field(ID, graphql_name='groupCategoryId')
    omit_from_final_grade = sgqlc.types.Field(Boolean, graphql_name='omitFromFinalGrade')
    anonymous_instructor_annotations = sgqlc.types.Field(Boolean, graphql_name='anonymousInstructorAnnotations')
    post_to_sis = sgqlc.types.Field(Boolean, graphql_name='postToSis')
    anonymous_grading = sgqlc.types.Field(Boolean, graphql_name='anonymousGrading')
    module_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='moduleIds')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')


class UpdateCommentBankItemInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('id', 'comment')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    comment = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='comment')


class UpdateConversationParticipantsInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('conversation_ids', 'starred', 'subscribed', 'workflow_state')
    conversation_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='conversationIds')
    starred = sgqlc.types.Field(Boolean, graphql_name='starred')
    subscribed = sgqlc.types.Field(Boolean, graphql_name='subscribed')
    workflow_state = sgqlc.types.Field(String, graphql_name='workflowState')


class UpdateDiscussionEntriesReadStateInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('discussion_entry_ids', 'read')
    discussion_entry_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='discussionEntryIds')
    read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='read')


class UpdateDiscussionEntryInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('discussion_entry_id', 'message', 'remove_attachment', 'file_id', 'quoted_entry_id')
    discussion_entry_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='discussionEntryId')
    message = sgqlc.types.Field(String, graphql_name='message')
    remove_attachment = sgqlc.types.Field(Boolean, graphql_name='removeAttachment')
    file_id = sgqlc.types.Field(ID, graphql_name='fileId')
    quoted_entry_id = sgqlc.types.Field(ID, graphql_name='quotedEntryId')


class UpdateDiscussionEntryParticipantInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('discussion_entry_id', 'read', 'rating', 'forced_read_state', 'report_type')
    discussion_entry_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='discussionEntryId')
    read = sgqlc.types.Field(Boolean, graphql_name='read')
    rating = sgqlc.types.Field(RatingInputType, graphql_name='rating')
    forced_read_state = sgqlc.types.Field(Boolean, graphql_name='forcedReadState')
    report_type = sgqlc.types.Field(ReportType, graphql_name='reportType')


class UpdateDiscussionReadStateInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('discussion_topic_id', 'read')
    discussion_topic_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='discussionTopicId')
    read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='read')


class UpdateDiscussionThreadReadStateInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('discussion_entry_id', 'read')
    discussion_entry_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='discussionEntryId')
    read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='read')


class UpdateDiscussionTopicInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('allow_rating', 'delayed_post_at', 'group_category_id', 'lock_at', 'locked', 'message', 'only_graders_can_rate', 'published', 'require_initial_post', 'title', 'todo_date', 'podcast_enabled', 'podcast_has_student_posts', 'specific_sections', 'file_id', 'discussion_topic_id', 'remove_attachment', 'assignment')
    allow_rating = sgqlc.types.Field(Boolean, graphql_name='allowRating')
    delayed_post_at = sgqlc.types.Field(DateTime, graphql_name='delayedPostAt')
    group_category_id = sgqlc.types.Field(ID, graphql_name='groupCategoryId')
    lock_at = sgqlc.types.Field(DateTime, graphql_name='lockAt')
    locked = sgqlc.types.Field(Boolean, graphql_name='locked')
    message = sgqlc.types.Field(String, graphql_name='message')
    only_graders_can_rate = sgqlc.types.Field(Boolean, graphql_name='onlyGradersCanRate')
    published = sgqlc.types.Field(Boolean, graphql_name='published')
    require_initial_post = sgqlc.types.Field(Boolean, graphql_name='requireInitialPost')
    title = sgqlc.types.Field(String, graphql_name='title')
    todo_date = sgqlc.types.Field(DateTime, graphql_name='todoDate')
    podcast_enabled = sgqlc.types.Field(Boolean, graphql_name='podcastEnabled')
    podcast_has_student_posts = sgqlc.types.Field(Boolean, graphql_name='podcastHasStudentPosts')
    specific_sections = sgqlc.types.Field(String, graphql_name='specificSections')
    file_id = sgqlc.types.Field(ID, graphql_name='fileId')
    discussion_topic_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='discussionTopicId')
    remove_attachment = sgqlc.types.Field(Boolean, graphql_name='removeAttachment')
    assignment = sgqlc.types.Field(AssignmentUpdate, graphql_name='assignment')


class UpdateInternalSettingInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('internal_setting_id', 'value')
    internal_setting_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='internalSettingId')
    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='value')


class UpdateIsolatedViewDeeplyNestedAlertInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('isolated_view_deeply_nested_alert',)
    isolated_view_deeply_nested_alert = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isolatedViewDeeplyNestedAlert')


class UpdateLearningOutcomeGroupInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('id', 'title', 'description', 'vendor_guid', 'parent_outcome_group_id')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    title = sgqlc.types.Field(String, graphql_name='title')
    description = sgqlc.types.Field(String, graphql_name='description')
    vendor_guid = sgqlc.types.Field(String, graphql_name='vendorGuid')
    parent_outcome_group_id = sgqlc.types.Field(ID, graphql_name='parentOutcomeGroupId')


class UpdateLearningOutcomeInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('title', 'description', 'display_name', 'vendor_guid', 'calculation_method', 'calculation_int', 'mastery_points', 'ratings', 'id')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    description = sgqlc.types.Field(String, graphql_name='description')
    display_name = sgqlc.types.Field(String, graphql_name='displayName')
    vendor_guid = sgqlc.types.Field(String, graphql_name='vendorGuid')
    calculation_method = sgqlc.types.Field(String, graphql_name='calculationMethod')
    calculation_int = sgqlc.types.Field(Int, graphql_name='calculationInt')
    mastery_points = sgqlc.types.Field(Float, graphql_name='masteryPoints')
    ratings = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ProficiencyRatingInput)), graphql_name='ratings')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')


class UpdateNotificationPreferencesInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('account_id', 'course_id', 'context_type', 'enabled', 'has_read_privacy_notice', 'send_scores_in_emails', 'send_observed_names_in_notifications', 'communication_channel_id', 'notification_category', 'frequency', 'is_policy_override')
    account_id = sgqlc.types.Field(ID, graphql_name='accountId')
    course_id = sgqlc.types.Field(ID, graphql_name='courseId')
    context_type = sgqlc.types.Field(sgqlc.types.non_null(NotificationPreferencesContextType), graphql_name='contextType')
    enabled = sgqlc.types.Field(Boolean, graphql_name='enabled')
    has_read_privacy_notice = sgqlc.types.Field(Boolean, graphql_name='hasReadPrivacyNotice')
    send_scores_in_emails = sgqlc.types.Field(Boolean, graphql_name='sendScoresInEmails')
    send_observed_names_in_notifications = sgqlc.types.Field(Boolean, graphql_name='sendObservedNamesInNotifications')
    communication_channel_id = sgqlc.types.Field(ID, graphql_name='communicationChannelId')
    notification_category = sgqlc.types.Field(NotificationCategoryType, graphql_name='notificationCategory')
    frequency = sgqlc.types.Field(NotificationFrequencyType, graphql_name='frequency')
    is_policy_override = sgqlc.types.Field(Boolean, graphql_name='isPolicyOverride')


class UpdateOutcomeCalculationMethodInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('id', 'calculation_method', 'calculation_int')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    calculation_method = sgqlc.types.Field(String, graphql_name='calculationMethod')
    calculation_int = sgqlc.types.Field(Int, graphql_name='calculationInt')


class UpdateOutcomeProficiencyInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('id', 'proficiency_ratings')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    proficiency_ratings = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(OutcomeProficiencyRatingCreate)), graphql_name='proficiencyRatings')


class UpdateRubricArchivedStateInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('archived', 'id')
    archived = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='archived')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')


class UpdateSubmissionStudentEnteredScoreInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('entered_score', 'submission_id')
    entered_score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='enteredScore')
    submission_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='submissionId')


class UpdateSubmissionsGradeInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('submission_id', 'score')
    submission_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='submissionId')
    score = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='score')


class UpdateSubmissionsReadStateInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('submission_ids', 'read')
    submission_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='submissionIds')
    read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='read')


class UpdateUserDiscussionsSplitscreenViewInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('discussions_splitscreen_view',)
    discussions_splitscreen_view = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='discussionsSplitscreenView')


class UpsertCustomGradeStatusInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('color', 'id', 'name')
    color = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='color')
    id = sgqlc.types.Field(ID, graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')


class UpsertStandardGradeStatusInput(sgqlc.types.Input):
    __schema__ = canvas_schema
    __field_names__ = ('color', 'id', 'name')
    color = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='color')
    id = sgqlc.types.Field(ID, graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')



########################################################################
# Output Objects and Interfaces
########################################################################
class AssetString(sgqlc.types.Interface):
    __schema__ = canvas_schema
    __field_names__ = ('asset_string',)
    asset_string = sgqlc.types.Field(String, graphql_name='assetString')


class AssignmentsConnectionInterface(sgqlc.types.Interface):
    __schema__ = canvas_schema
    __field_names__ = ('assignments_connection',)
    assignments_connection = sgqlc.types.Field('AssignmentConnection', graphql_name='assignmentsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
        ('filter', sgqlc.types.Arg(AssignmentFilter, graphql_name='filter', default=None)),
))
    )


class LegacyIDInterface(sgqlc.types.Interface):
    __schema__ = canvas_schema
    __field_names__ = ('_id',)
    _id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='_id')


class ModuleItemInterface(sgqlc.types.Interface):
    __schema__ = canvas_schema
    __field_names__ = ('modules',)
    modules = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('Module')), graphql_name='modules')


class Node(sgqlc.types.Interface):
    __schema__ = canvas_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')


class SubmissionInterface(sgqlc.types.Interface):
    __schema__ = canvas_schema
    __field_names__ = ('assigned_assessments', 'assignment', 'assignment_id', 'attachment', 'attachments', 'attempt', 'body', 'comments_connection', 'custom_grade_status', 'deducted_points', 'entered_grade', 'entered_score', 'excused', 'extra_attempts', 'feedback_for_current_attempt', 'grade', 'grade_hidden', 'grade_matches_current_submission', 'graded_anonymously', 'graded_at', 'grading_status', 'hide_grade_from_student', 'late', 'late_policy_status', 'media_object', 'missing', 'originality_data', 'posted', 'posted_at', 'proxy_submitter', 'proxy_submitter_id', 'resource_link_lookup_uuid', 'rubric_assessments_connection', 'score', 'state', 'sticker', 'submission_draft', 'submission_status', 'submission_type', 'submitted_at', 'turnitin_data', 'unread_comment_count', 'url', 'user')
    assigned_assessments = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('AssessmentRequest')), graphql_name='assignedAssessments')
    assignment = sgqlc.types.Field('Assignment', graphql_name='assignment')
    assignment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assignmentId')
    attachment = sgqlc.types.Field('File', graphql_name='attachment')
    attachments = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('File')), graphql_name='attachments')
    attempt = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='attempt')
    body = sgqlc.types.Field(String, graphql_name='body')
    comments_connection = sgqlc.types.Field('SubmissionCommentConnection', graphql_name='commentsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
        ('filter', sgqlc.types.Arg(SubmissionCommentFilterInput, graphql_name='filter', default={})),
        ('sort_order', sgqlc.types.Arg(SubmissionCommentsSortOrderType, graphql_name='sortOrder', default=None)),
))
    )
    custom_grade_status = sgqlc.types.Field(String, graphql_name='customGradeStatus')
    deducted_points = sgqlc.types.Field(Float, graphql_name='deductedPoints')
    entered_grade = sgqlc.types.Field(String, graphql_name='enteredGrade')
    entered_score = sgqlc.types.Field(Float, graphql_name='enteredScore')
    excused = sgqlc.types.Field(Boolean, graphql_name='excused')
    extra_attempts = sgqlc.types.Field(Int, graphql_name='extraAttempts')
    feedback_for_current_attempt = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='feedbackForCurrentAttempt')
    grade = sgqlc.types.Field(String, graphql_name='grade')
    grade_hidden = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='gradeHidden')
    grade_matches_current_submission = sgqlc.types.Field(Boolean, graphql_name='gradeMatchesCurrentSubmission')
    graded_anonymously = sgqlc.types.Field(Boolean, graphql_name='gradedAnonymously')
    graded_at = sgqlc.types.Field(DateTime, graphql_name='gradedAt')
    grading_status = sgqlc.types.Field(SubmissionGradingStatus, graphql_name='gradingStatus')
    hide_grade_from_student = sgqlc.types.Field(Boolean, graphql_name='hideGradeFromStudent')
    late = sgqlc.types.Field(Boolean, graphql_name='late')
    late_policy_status = sgqlc.types.Field(LatePolicyStatusType, graphql_name='latePolicyStatus')
    media_object = sgqlc.types.Field('MediaObject', graphql_name='mediaObject')
    missing = sgqlc.types.Field(Boolean, graphql_name='missing')
    originality_data = sgqlc.types.Field(JSON, graphql_name='originalityData')
    posted = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='posted')
    posted_at = sgqlc.types.Field(DateTime, graphql_name='postedAt')
    proxy_submitter = sgqlc.types.Field(String, graphql_name='proxySubmitter')
    proxy_submitter_id = sgqlc.types.Field(ID, graphql_name='proxySubmitterId')
    resource_link_lookup_uuid = sgqlc.types.Field(String, graphql_name='resourceLinkLookupUuid')
    rubric_assessments_connection = sgqlc.types.Field('RubricAssessmentConnection', graphql_name='rubricAssessmentsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
        ('filter', sgqlc.types.Arg(SubmissionRubricAssessmentFilterInput, graphql_name='filter', default={})),
))
    )
    score = sgqlc.types.Field(Float, graphql_name='score')
    state = sgqlc.types.Field(sgqlc.types.non_null(SubmissionState), graphql_name='state')
    sticker = sgqlc.types.Field(String, graphql_name='sticker')
    submission_draft = sgqlc.types.Field('SubmissionDraft', graphql_name='submissionDraft')
    submission_status = sgqlc.types.Field(String, graphql_name='submissionStatus')
    submission_type = sgqlc.types.Field(SubmissionType, graphql_name='submissionType')
    submitted_at = sgqlc.types.Field(DateTime, graphql_name='submittedAt')
    turnitin_data = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('TurnitinData')), graphql_name='turnitinData')
    unread_comment_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='unreadCommentCount')
    url = sgqlc.types.Field(URL, graphql_name='url')
    user = sgqlc.types.Field('User', graphql_name='user')


class Timestamped(sgqlc.types.Interface):
    __schema__ = canvas_schema
    __field_names__ = ('created_at', 'updated_at')
    created_at = sgqlc.types.Field(DateTime, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')


class AccountConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('AccountEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('Account'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class AccountEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('Account', graphql_name='node')


class AddConversationMessagePayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('conversation_message', 'errors')
    conversation_message = sgqlc.types.Field('ConversationMessage', graphql_name='conversationMessage')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class AdhocStudents(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('students',)
    students = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('User')), graphql_name='students')


class AnonymousUser(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('avatar_url', 'id', 'short_name')
    avatar_url = sgqlc.types.Field(String, graphql_name='avatarUrl')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    short_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='shortName')


class AssignmentConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('AssignmentEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('Assignment'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class AssignmentEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('Assignment', graphql_name='node')


class AssignmentGroupConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('AssignmentGroupEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('AssignmentGroup'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class AssignmentGroupEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('AssignmentGroup', graphql_name='node')


class AssignmentGroupRules(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('drop_highest', 'drop_lowest', 'never_drop')
    drop_highest = sgqlc.types.Field(Int, graphql_name='dropHighest')
    drop_lowest = sgqlc.types.Field(Int, graphql_name='dropLowest')
    never_drop = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('Assignment')), graphql_name='neverDrop')


class AssignmentOverrideConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('AssignmentOverrideEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('AssignmentOverride'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class AssignmentOverrideEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('AssignmentOverride', graphql_name='node')


class AssignmentScoreStatistic(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('count', 'lower_q', 'maximum', 'mean', 'median', 'minimum', 'upper_q')
    count = sgqlc.types.Field(Int, graphql_name='count')
    lower_q = sgqlc.types.Field(Float, graphql_name='lowerQ')
    maximum = sgqlc.types.Field(Float, graphql_name='maximum')
    mean = sgqlc.types.Field(Float, graphql_name='mean')
    median = sgqlc.types.Field(Float, graphql_name='median')
    minimum = sgqlc.types.Field(Float, graphql_name='minimum')
    upper_q = sgqlc.types.Field(Float, graphql_name='upperQ')


class AuditLogs(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('mutation_logs',)
    mutation_logs = sgqlc.types.Field('MutationLogConnection', graphql_name='mutationLogs', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
        ('asset_string', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='assetString', default=None)),
        ('start_time', sgqlc.types.Arg(DateTime, graphql_name='startTime', default=None)),
        ('end_time', sgqlc.types.Arg(DateTime, graphql_name='endTime', default=None)),
))
    )


class Checkpoint(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('due_at', 'label', 'name', 'only_visible_to_overrides', 'points_possible')
    due_at = sgqlc.types.Field(DateTime, graphql_name='dueAt')
    label = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='label')
    name = sgqlc.types.Field(String, graphql_name='name')
    only_visible_to_overrides = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='onlyVisibleToOverrides')
    points_possible = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='pointsPossible')


class CommentBankItemConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('CommentBankItemEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('CommentBankItem'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class CommentBankItemEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('CommentBankItem', graphql_name='node')


class ContentTagConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('ContentTag'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('ContentTagContent'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class ConversationMessage(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('_id', 'attachments_connection', 'author', 'body', 'conversation_id', 'created_at', 'id', 'media_comment', 'recipients')
    _id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='_id')
    attachments_connection = sgqlc.types.Field('FileConnection', graphql_name='attachmentsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    author = sgqlc.types.Field('User', graphql_name='author')
    body = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='body')
    conversation_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='conversationId')
    created_at = sgqlc.types.Field(DateTime, graphql_name='createdAt')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    media_comment = sgqlc.types.Field('MediaObject', graphql_name='mediaComment')
    recipients = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('User'))), graphql_name='recipients')


class ConversationMessageConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('ConversationMessageEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of(ConversationMessage), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class ConversationMessageEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(ConversationMessage, graphql_name='node')


class ConversationParticipant(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('_id', 'conversation', 'id', 'label', 'messages', 'subscribed', 'updated_at', 'user', 'user_id', 'workflow_state')
    _id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='_id')
    conversation = sgqlc.types.Field('Conversation', graphql_name='conversation')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    label = sgqlc.types.Field(String, graphql_name='label')
    messages = sgqlc.types.Field(ConversationMessageConnection, graphql_name='messages', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    subscribed = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='subscribed')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    user = sgqlc.types.Field('User', graphql_name='user')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='userId')
    workflow_state = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='workflowState')


class ConversationParticipantConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('ConversationParticipantEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of(ConversationParticipant), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class ConversationParticipantEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(ConversationParticipant, graphql_name='node')


class CourseConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('CourseEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('Course'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class CourseEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('Course', graphql_name='node')


class CourseOutcomeAlignmentStats(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('aligned_artifacts', 'aligned_outcomes', 'artifact_alignments', 'total_alignments', 'total_artifacts', 'total_outcomes')
    aligned_artifacts = sgqlc.types.Field(Int, graphql_name='alignedArtifacts')
    aligned_outcomes = sgqlc.types.Field(Int, graphql_name='alignedOutcomes')
    artifact_alignments = sgqlc.types.Field(Int, graphql_name='artifactAlignments')
    total_alignments = sgqlc.types.Field(Int, graphql_name='totalAlignments')
    total_artifacts = sgqlc.types.Field(Int, graphql_name='totalArtifacts')
    total_outcomes = sgqlc.types.Field(Int, graphql_name='totalOutcomes')


class CoursePermissions(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('become_user', 'manage_grades', 'send_messages', 'view_all_grades', 'view_analytics')
    become_user = sgqlc.types.Field(Boolean, graphql_name='becomeUser')
    manage_grades = sgqlc.types.Field(Boolean, graphql_name='manageGrades')
    send_messages = sgqlc.types.Field(Boolean, graphql_name='sendMessages')
    view_all_grades = sgqlc.types.Field(Boolean, graphql_name='viewAllGrades')
    view_analytics = sgqlc.types.Field(Boolean, graphql_name='viewAnalytics')


class CreateAccountDomainLookupPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('account_domain_lookup', 'errors')
    account_domain_lookup = sgqlc.types.Field('AccountDomainLookup', graphql_name='accountDomainLookup')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class CreateAssignmentPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('assignment', 'errors')
    assignment = sgqlc.types.Field('Assignment', graphql_name='assignment')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class CreateCommentBankItemPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('comment_bank_item', 'errors')
    comment_bank_item = sgqlc.types.Field('CommentBankItem', graphql_name='commentBankItem')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class CreateConversationPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('conversations', 'errors')
    conversations = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ConversationParticipant)), graphql_name='conversations')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class CreateDiscussionEntryDraftPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('discussion_entry_draft', 'errors')
    discussion_entry_draft = sgqlc.types.Field('DiscussionEntryDraft', graphql_name='discussionEntryDraft')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class CreateDiscussionEntryPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('discussion_entry', 'errors')
    discussion_entry = sgqlc.types.Field('DiscussionEntry', graphql_name='discussionEntry')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class CreateDiscussionTopicPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('discussion_topic', 'errors')
    discussion_topic = sgqlc.types.Field('Discussion', graphql_name='discussionTopic')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class CreateGroupInSetPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'group')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    group = sgqlc.types.Field('Group', graphql_name='group')


class CreateInternalSettingPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'internal_setting')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    internal_setting = sgqlc.types.Field('InternalSetting', graphql_name='internalSetting')


class CreateLearningOutcomeGroupPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'learning_outcome_group')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    learning_outcome_group = sgqlc.types.Field('LearningOutcomeGroup', graphql_name='learningOutcomeGroup')


class CreateLearningOutcomePayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'learning_outcome')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    learning_outcome = sgqlc.types.Field('LearningOutcome', graphql_name='learningOutcome')


class CreateModulePayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'module')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    module = sgqlc.types.Field('Module', graphql_name='module')


class CreateOutcomeCalculationMethodPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'outcome_calculation_method')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    outcome_calculation_method = sgqlc.types.Field('OutcomeCalculationMethod', graphql_name='outcomeCalculationMethod')


class CreateOutcomeProficiencyPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'outcome_proficiency')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    outcome_proficiency = sgqlc.types.Field('OutcomeProficiency', graphql_name='outcomeProficiency')


class CreateSubmissionCommentPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'submission_comment')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    submission_comment = sgqlc.types.Field('SubmissionComment', graphql_name='submissionComment')


class CreateSubmissionDraftPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'submission_draft')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    submission_draft = sgqlc.types.Field('SubmissionDraft', graphql_name='submissionDraft')


class CreateSubmissionPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'submission')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    submission = sgqlc.types.Field('Submission', graphql_name='submission')


class CreateUserInboxLabelPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'inbox_labels')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    inbox_labels = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='inboxLabels')


class CustomGradeStatusConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('CustomGradeStatusEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('CustomGradeStatus'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class CustomGradeStatusEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('CustomGradeStatus', graphql_name='node')


class DeleteAccountDomainLookupPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('account_domain_lookup_id', 'errors')
    account_domain_lookup_id = sgqlc.types.Field(ID, graphql_name='accountDomainLookupId')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class DeleteCommentBankItemPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('comment_bank_item_id', 'errors')
    comment_bank_item_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='commentBankItemId')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class DeleteConversationMessagesPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('conversation_message_ids', 'errors')
    conversation_message_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='conversationMessageIds')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class DeleteConversationsPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('conversation_ids', 'errors')
    conversation_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='conversationIds')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class DeleteCustomGradeStatusPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('custom_grade_status_id', 'errors')
    custom_grade_status_id = sgqlc.types.Field(ID, graphql_name='customGradeStatusId')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class DeleteDiscussionEntryPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('discussion_entry', 'errors')
    discussion_entry = sgqlc.types.Field('DiscussionEntry', graphql_name='discussionEntry')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class DeleteDiscussionTopicPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('discussion_topic_id', 'errors')
    discussion_topic_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='discussionTopicId')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class DeleteInternalSettingPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'internal_setting_id')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    internal_setting_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='internalSettingId')


class DeleteOutcomeCalculationMethodPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'outcome_calculation_method_id')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    outcome_calculation_method_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='outcomeCalculationMethodId')


class DeleteOutcomeLinksPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('deleted_outcome_link_ids', 'errors')
    deleted_outcome_link_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='deletedOutcomeLinkIds')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class DeleteOutcomeProficiencyPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'outcome_proficiency_id')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    outcome_proficiency_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='outcomeProficiencyId')


class DeleteSubmissionDraftPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'submission_draft_ids')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    submission_draft_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='submissionDraftIds')


class DeleteUserInboxLabelPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'inbox_labels')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    inbox_labels = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='inboxLabels')


class DiscussionEntryConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('DiscussionEntryEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('DiscussionEntry'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class DiscussionEntryCounts(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('deleted_count', 'replies_count', 'unread_count')
    deleted_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='deletedCount')
    replies_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='repliesCount')
    unread_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='unreadCount')


class DiscussionEntryDraftConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('DiscussionEntryDraftEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('DiscussionEntryDraft'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class DiscussionEntryDraftEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('DiscussionEntryDraft', graphql_name='node')


class DiscussionEntryEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('DiscussionEntry', graphql_name='node')


class DiscussionEntryPermissions(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('attach', 'create', 'delete', 'rate', 'read', 'reply', 'update', 'view_rating')
    attach = sgqlc.types.Field(Boolean, graphql_name='attach')
    create = sgqlc.types.Field(Boolean, graphql_name='create')
    delete = sgqlc.types.Field(Boolean, graphql_name='delete')
    rate = sgqlc.types.Field(Boolean, graphql_name='rate')
    read = sgqlc.types.Field(Boolean, graphql_name='read')
    reply = sgqlc.types.Field(Boolean, graphql_name='reply')
    update = sgqlc.types.Field(Boolean, graphql_name='update')
    view_rating = sgqlc.types.Field(Boolean, graphql_name='viewRating')


class DiscussionEntryReportTypeCounts(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('inappropriate_count', 'offensive_count', 'other_count', 'total')
    inappropriate_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='inappropriateCount')
    offensive_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='offensiveCount')
    other_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='otherCount')
    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')


class DiscussionEntryVersionConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('DiscussionEntryVersionEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('DiscussionEntryVersion'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class DiscussionEntryVersionEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('DiscussionEntryVersion', graphql_name='node')


class DiscussionPermissions(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('add_rubric', 'attach', 'close_for_comments', 'copy_and_send_to', 'create', 'delete', 'duplicate', 'manage_content', 'manage_course_content_add', 'manage_course_content_delete', 'manage_course_content_edit', 'moderate_forum', 'open_for_comments', 'peer_review', 'rate', 'read', 'read_as_admin', 'read_replies', 'reply', 'show_rubric', 'speed_grader', 'student_reporting', 'update')
    add_rubric = sgqlc.types.Field(Boolean, graphql_name='addRubric')
    attach = sgqlc.types.Field(Boolean, graphql_name='attach')
    close_for_comments = sgqlc.types.Field(Boolean, graphql_name='closeForComments')
    copy_and_send_to = sgqlc.types.Field(Boolean, graphql_name='copyAndSendTo')
    create = sgqlc.types.Field(Boolean, graphql_name='create')
    delete = sgqlc.types.Field(Boolean, graphql_name='delete')
    duplicate = sgqlc.types.Field(Boolean, graphql_name='duplicate')
    manage_content = sgqlc.types.Field(Boolean, graphql_name='manageContent')
    manage_course_content_add = sgqlc.types.Field(Boolean, graphql_name='manageCourseContentAdd')
    manage_course_content_delete = sgqlc.types.Field(Boolean, graphql_name='manageCourseContentDelete')
    manage_course_content_edit = sgqlc.types.Field(Boolean, graphql_name='manageCourseContentEdit')
    moderate_forum = sgqlc.types.Field(Boolean, graphql_name='moderateForum')
    open_for_comments = sgqlc.types.Field(Boolean, graphql_name='openForComments')
    peer_review = sgqlc.types.Field(Boolean, graphql_name='peerReview')
    rate = sgqlc.types.Field(Boolean, graphql_name='rate')
    read = sgqlc.types.Field(Boolean, graphql_name='read')
    read_as_admin = sgqlc.types.Field(Boolean, graphql_name='readAsAdmin')
    read_replies = sgqlc.types.Field(Boolean, graphql_name='readReplies')
    reply = sgqlc.types.Field(Boolean, graphql_name='reply')
    show_rubric = sgqlc.types.Field(Boolean, graphql_name='showRubric')
    speed_grader = sgqlc.types.Field(Boolean, graphql_name='speedGrader')
    student_reporting = sgqlc.types.Field(Boolean, graphql_name='studentReporting')
    update = sgqlc.types.Field(Boolean, graphql_name='update')


class EnrollmentConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('EnrollmentEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('Enrollment'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class EnrollmentEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('Enrollment', graphql_name='node')


class EntryParticipant(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('forced_read_state', 'rating', 'read', 'report_type')
    forced_read_state = sgqlc.types.Field(Boolean, graphql_name='forcedReadState')
    rating = sgqlc.types.Field(Boolean, graphql_name='rating')
    read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='read')
    report_type = sgqlc.types.Field(String, graphql_name='reportType')


class ExternalToolConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('ExternalToolEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('ExternalTool'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class ExternalToolEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('ExternalTool', graphql_name='node')


class ExternalToolPlacements(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('canvas_icon_class', 'icon_url', 'message_type', 'text', 'url')
    canvas_icon_class = sgqlc.types.Field(String, graphql_name='canvasIconClass')
    icon_url = sgqlc.types.Field(URL, graphql_name='iconUrl')
    message_type = sgqlc.types.Field(String, graphql_name='messageType')
    text = sgqlc.types.Field(String, graphql_name='text')
    url = sgqlc.types.Field(URL, graphql_name='url')


class ExternalToolSettings(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('homework_submission', 'icon_url', 'selection_height', 'selection_width', 'text')
    homework_submission = sgqlc.types.Field(ExternalToolPlacements, graphql_name='homeworkSubmission')
    icon_url = sgqlc.types.Field(URL, graphql_name='iconUrl')
    selection_height = sgqlc.types.Field(Int, graphql_name='selectionHeight')
    selection_width = sgqlc.types.Field(Int, graphql_name='selectionWidth')
    text = sgqlc.types.Field(String, graphql_name='text')


class FileConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('FileEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('File'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class FileEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('File', graphql_name='node')


class Grades(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('assignment_group', 'current_grade', 'current_score', 'custom_grade_status_id', 'enrollment', 'final_grade', 'final_score', 'grading_period', 'override_grade', 'override_score', 'state', 'unposted_current_grade', 'unposted_current_score', 'unposted_final_grade', 'unposted_final_score')
    assignment_group = sgqlc.types.Field('AssignmentGroup', graphql_name='assignmentGroup')
    current_grade = sgqlc.types.Field(String, graphql_name='currentGrade')
    current_score = sgqlc.types.Field(Float, graphql_name='currentScore')
    custom_grade_status_id = sgqlc.types.Field(ID, graphql_name='customGradeStatusId')
    enrollment = sgqlc.types.Field('Enrollment', graphql_name='enrollment')
    final_grade = sgqlc.types.Field(String, graphql_name='finalGrade')
    final_score = sgqlc.types.Field(Float, graphql_name='finalScore')
    grading_period = sgqlc.types.Field('GradingPeriod', graphql_name='gradingPeriod')
    override_grade = sgqlc.types.Field(String, graphql_name='overrideGrade')
    override_score = sgqlc.types.Field(Float, graphql_name='overrideScore')
    state = sgqlc.types.Field(sgqlc.types.non_null(GradeState), graphql_name='state')
    unposted_current_grade = sgqlc.types.Field(String, graphql_name='unpostedCurrentGrade')
    unposted_current_score = sgqlc.types.Field(Float, graphql_name='unpostedCurrentScore')
    unposted_final_grade = sgqlc.types.Field(String, graphql_name='unpostedFinalGrade')
    unposted_final_score = sgqlc.types.Field(Float, graphql_name='unpostedFinalScore')


class GradesConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('GradesEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of(Grades), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class GradesEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(Grades, graphql_name='node')


class GradingPeriodConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('GradingPeriodEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('GradingPeriod'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class GradingPeriodEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('GradingPeriod', graphql_name='node')


class GradingStandard(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('context_code', 'context_id', 'context_type', 'created_at', 'data', 'id', 'migration_id', 'root_account_id', 'title', 'updated_at', 'usage_count', 'user_id', 'version', 'workflow_state')
    context_code = sgqlc.types.Field(String, graphql_name='contextCode')
    context_id = sgqlc.types.Field(ID, graphql_name='contextId')
    context_type = sgqlc.types.Field(String, graphql_name='contextType')
    created_at = sgqlc.types.Field(DateTime, graphql_name='createdAt')
    data = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('GradingStandardItem')), graphql_name='data')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    migration_id = sgqlc.types.Field(ID, graphql_name='migrationId')
    root_account_id = sgqlc.types.Field(ID, graphql_name='rootAccountId')
    title = sgqlc.types.Field(String, graphql_name='title')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    usage_count = sgqlc.types.Field(Int, graphql_name='usageCount')
    user_id = sgqlc.types.Field(ID, graphql_name='userId')
    version = sgqlc.types.Field(Int, graphql_name='version')
    workflow_state = sgqlc.types.Field(String, graphql_name='workflowState')


class GradingStandardItem(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('base_value', 'letter_grade')
    base_value = sgqlc.types.Field(Float, graphql_name='baseValue')
    letter_grade = sgqlc.types.Field(String, graphql_name='letterGrade')


class GroupConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('GroupEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('Group'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class GroupEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('Group', graphql_name='node')


class GroupMembershipConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('GroupMembershipEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('GroupMembership'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class GroupMembershipEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('GroupMembership', graphql_name='node')


class GroupSetConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('GroupSetEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('GroupSet'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class GroupSetEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('GroupSet', graphql_name='node')


class HideAssignmentGradesForSectionsPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('assignment', 'errors', 'progress', 'sections')
    assignment = sgqlc.types.Field('Assignment', graphql_name='assignment')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    progress = sgqlc.types.Field('Progress', graphql_name='progress')
    sections = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('Section')), graphql_name='sections')


class HideAssignmentGradesPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('assignment', 'errors', 'progress', 'sections')
    assignment = sgqlc.types.Field('Assignment', graphql_name='assignment')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    progress = sgqlc.types.Field('Progress', graphql_name='progress')
    sections = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('Section')), graphql_name='sections')


class ImportOutcomesPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'progress')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    progress = sgqlc.types.Field('Progress', graphql_name='progress')


class LearningOutcomeGroupConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('LearningOutcomeGroupEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('LearningOutcomeGroup'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class LearningOutcomeGroupEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('LearningOutcomeGroup', graphql_name='node')


class LockInfo(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('can_view', 'is_locked', 'lock_at', 'locked_object', 'module', 'unlock_at')
    can_view = sgqlc.types.Field(Boolean, graphql_name='canView')
    is_locked = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isLocked')
    lock_at = sgqlc.types.Field(DateTime, graphql_name='lockAt')
    locked_object = sgqlc.types.Field('Lockable', graphql_name='lockedObject')
    module = sgqlc.types.Field('Module', graphql_name='module')
    unlock_at = sgqlc.types.Field(DateTime, graphql_name='unlockAt')


class MarkSubmissionCommentsReadPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'submission_comments')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    submission_comments = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('SubmissionComment')), graphql_name='submissionComments')


class MediaSource(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('bitrate', 'content_type', 'file_ext', 'height', 'is_original', 'size', 'url', 'width')
    bitrate = sgqlc.types.Field(String, graphql_name='bitrate')
    content_type = sgqlc.types.Field(String, graphql_name='contentType')
    file_ext = sgqlc.types.Field(String, graphql_name='fileExt')
    height = sgqlc.types.Field(String, graphql_name='height')
    is_original = sgqlc.types.Field(String, graphql_name='isOriginal')
    size = sgqlc.types.Field(String, graphql_name='size')
    url = sgqlc.types.Field(URL, graphql_name='url')
    width = sgqlc.types.Field(String, graphql_name='width')


class MessagePermissions(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('send_messages', 'send_messages_all')
    send_messages = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='sendMessages')
    send_messages_all = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='sendMessagesAll')


class MessageableContextConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('MessageableContextEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('MessageableContext'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class MessageableContextEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('MessageableContext', graphql_name='node')


class MessageableUserConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('MessageableUserEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('MessageableUser'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class MessageableUserEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('MessageableUser', graphql_name='node')


class ModeratedGrading(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('enabled', 'final_grader', 'grader_comments_visible_to_graders', 'grader_count', 'grader_names_visible_to_final_grader', 'graders_anonymous_to_graders')
    enabled = sgqlc.types.Field(Boolean, graphql_name='enabled')
    final_grader = sgqlc.types.Field('User', graphql_name='finalGrader')
    grader_comments_visible_to_graders = sgqlc.types.Field(Boolean, graphql_name='graderCommentsVisibleToGraders')
    grader_count = sgqlc.types.Field(Int, graphql_name='graderCount')
    grader_names_visible_to_final_grader = sgqlc.types.Field(Boolean, graphql_name='graderNamesVisibleToFinalGrader')
    graders_anonymous_to_graders = sgqlc.types.Field(Boolean, graphql_name='gradersAnonymousToGraders')


class ModuleConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('ModuleEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('Module'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class ModuleEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('Module', graphql_name='node')


class MoveOutcomeLinksPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'moved_outcome_links')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    moved_outcome_links = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ContentTag'))), graphql_name='movedOutcomeLinks')


class Mutation(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('add_conversation_message', 'create_account_domain_lookup', 'create_assignment', 'create_comment_bank_item', 'create_conversation', 'create_discussion_entry', 'create_discussion_entry_draft', 'create_discussion_topic', 'create_group_in_set', 'create_internal_setting', 'create_learning_outcome', 'create_learning_outcome_group', 'create_module', 'create_outcome_calculation_method', 'create_outcome_proficiency', 'create_submission', 'create_submission_comment', 'create_submission_draft', 'create_user_inbox_label', 'delete_account_domain_lookup', 'delete_comment_bank_item', 'delete_conversation_messages', 'delete_conversations', 'delete_custom_grade_status', 'delete_discussion_entry', 'delete_discussion_topic', 'delete_internal_setting', 'delete_outcome_calculation_method', 'delete_outcome_links', 'delete_outcome_proficiency', 'delete_submission_draft', 'delete_user_inbox_label', 'hide_assignment_grades', 'hide_assignment_grades_for_sections', 'import_outcomes', 'mark_submission_comments_read', 'move_outcome_links', 'post_assignment_grades', 'post_assignment_grades_for_sections', 'set_assignment_post_policy', 'set_course_post_policy', 'set_friendly_description', 'set_module_item_completion', 'set_override_score', 'set_override_status', 'subscribe_to_discussion_topic', 'update_account_domain_lookup', 'update_assignment', 'update_comment_bank_item', 'update_conversation_participants', 'update_discussion_entries_read_state', 'update_discussion_entry', 'update_discussion_entry_participant', 'update_discussion_read_state', 'update_discussion_thread_read_state', 'update_discussion_topic', 'update_internal_setting', 'update_isolated_view_deeply_nested_alert', 'update_learning_outcome', 'update_learning_outcome_group', 'update_notification_preferences', 'update_outcome_calculation_method', 'update_outcome_proficiency', 'update_rubric_archived_state', 'update_submission_grade', 'update_submission_student_entered_score', 'update_submissions_read_state', 'update_user_discussions_splitscreen_view', 'upsert_custom_grade_status', 'upsert_standard_grade_status')
    add_conversation_message = sgqlc.types.Field(AddConversationMessagePayload, graphql_name='addConversationMessage', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(AddConversationMessageInput), graphql_name='input', default=None)),
))
    )
    create_account_domain_lookup = sgqlc.types.Field(CreateAccountDomainLookupPayload, graphql_name='createAccountDomainLookup', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateAccountDomainLookupInput), graphql_name='input', default=None)),
))
    )
    create_assignment = sgqlc.types.Field(CreateAssignmentPayload, graphql_name='createAssignment', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateAssignmentInput), graphql_name='input', default=None)),
))
    )
    create_comment_bank_item = sgqlc.types.Field(CreateCommentBankItemPayload, graphql_name='createCommentBankItem', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateCommentBankItemInput), graphql_name='input', default=None)),
))
    )
    create_conversation = sgqlc.types.Field(CreateConversationPayload, graphql_name='createConversation', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateConversationInput), graphql_name='input', default=None)),
))
    )
    create_discussion_entry = sgqlc.types.Field(CreateDiscussionEntryPayload, graphql_name='createDiscussionEntry', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateDiscussionEntryInput), graphql_name='input', default=None)),
))
    )
    create_discussion_entry_draft = sgqlc.types.Field(CreateDiscussionEntryDraftPayload, graphql_name='createDiscussionEntryDraft', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateDiscussionEntryDraftInput), graphql_name='input', default=None)),
))
    )
    create_discussion_topic = sgqlc.types.Field(CreateDiscussionTopicPayload, graphql_name='createDiscussionTopic', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateDiscussionTopicInput), graphql_name='input', default=None)),
))
    )
    create_group_in_set = sgqlc.types.Field(CreateGroupInSetPayload, graphql_name='createGroupInSet', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateGroupInSetInput), graphql_name='input', default=None)),
))
    )
    create_internal_setting = sgqlc.types.Field(CreateInternalSettingPayload, graphql_name='createInternalSetting', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateInternalSettingInput), graphql_name='input', default=None)),
))
    )
    create_learning_outcome = sgqlc.types.Field(CreateLearningOutcomePayload, graphql_name='createLearningOutcome', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateLearningOutcomeInput), graphql_name='input', default=None)),
))
    )
    create_learning_outcome_group = sgqlc.types.Field(CreateLearningOutcomeGroupPayload, graphql_name='createLearningOutcomeGroup', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateLearningOutcomeGroupInput), graphql_name='input', default=None)),
))
    )
    create_module = sgqlc.types.Field(CreateModulePayload, graphql_name='createModule', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateModuleInput), graphql_name='input', default=None)),
))
    )
    create_outcome_calculation_method = sgqlc.types.Field(CreateOutcomeCalculationMethodPayload, graphql_name='createOutcomeCalculationMethod', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateOutcomeCalculationMethodInput), graphql_name='input', default=None)),
))
    )
    create_outcome_proficiency = sgqlc.types.Field(CreateOutcomeProficiencyPayload, graphql_name='createOutcomeProficiency', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateOutcomeProficiencyInput), graphql_name='input', default=None)),
))
    )
    create_submission = sgqlc.types.Field(CreateSubmissionPayload, graphql_name='createSubmission', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateSubmissionInput), graphql_name='input', default=None)),
))
    )
    create_submission_comment = sgqlc.types.Field(CreateSubmissionCommentPayload, graphql_name='createSubmissionComment', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateSubmissionCommentInput), graphql_name='input', default=None)),
))
    )
    create_submission_draft = sgqlc.types.Field(CreateSubmissionDraftPayload, graphql_name='createSubmissionDraft', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateSubmissionDraftInput), graphql_name='input', default=None)),
))
    )
    create_user_inbox_label = sgqlc.types.Field(CreateUserInboxLabelPayload, graphql_name='createUserInboxLabel', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateUserInboxLabelInput), graphql_name='input', default=None)),
))
    )
    delete_account_domain_lookup = sgqlc.types.Field(DeleteAccountDomainLookupPayload, graphql_name='deleteAccountDomainLookup', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteAccountDomainLookupInput), graphql_name='input', default=None)),
))
    )
    delete_comment_bank_item = sgqlc.types.Field(DeleteCommentBankItemPayload, graphql_name='deleteCommentBankItem', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteCommentBankItemInput), graphql_name='input', default=None)),
))
    )
    delete_conversation_messages = sgqlc.types.Field(DeleteConversationMessagesPayload, graphql_name='deleteConversationMessages', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteConversationMessagesInput), graphql_name='input', default=None)),
))
    )
    delete_conversations = sgqlc.types.Field(DeleteConversationsPayload, graphql_name='deleteConversations', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteConversationsInput), graphql_name='input', default=None)),
))
    )
    delete_custom_grade_status = sgqlc.types.Field(DeleteCustomGradeStatusPayload, graphql_name='deleteCustomGradeStatus', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteCustomGradeStatusInput), graphql_name='input', default=None)),
))
    )
    delete_discussion_entry = sgqlc.types.Field(DeleteDiscussionEntryPayload, graphql_name='deleteDiscussionEntry', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteDiscussionEntryInput), graphql_name='input', default=None)),
))
    )
    delete_discussion_topic = sgqlc.types.Field(DeleteDiscussionTopicPayload, graphql_name='deleteDiscussionTopic', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteDiscussionTopicInput), graphql_name='input', default=None)),
))
    )
    delete_internal_setting = sgqlc.types.Field(DeleteInternalSettingPayload, graphql_name='deleteInternalSetting', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteInternalSettingInput), graphql_name='input', default=None)),
))
    )
    delete_outcome_calculation_method = sgqlc.types.Field(DeleteOutcomeCalculationMethodPayload, graphql_name='deleteOutcomeCalculationMethod', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteOutcomeCalculationMethodInput), graphql_name='input', default=None)),
))
    )
    delete_outcome_links = sgqlc.types.Field(DeleteOutcomeLinksPayload, graphql_name='deleteOutcomeLinks', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteOutcomeLinksInput), graphql_name='input', default=None)),
))
    )
    delete_outcome_proficiency = sgqlc.types.Field(DeleteOutcomeProficiencyPayload, graphql_name='deleteOutcomeProficiency', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteOutcomeProficiencyInput), graphql_name='input', default=None)),
))
    )
    delete_submission_draft = sgqlc.types.Field(DeleteSubmissionDraftPayload, graphql_name='deleteSubmissionDraft', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteSubmissionDraftInput), graphql_name='input', default=None)),
))
    )
    delete_user_inbox_label = sgqlc.types.Field(DeleteUserInboxLabelPayload, graphql_name='deleteUserInboxLabel', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteUserInboxLabelInput), graphql_name='input', default=None)),
))
    )
    hide_assignment_grades = sgqlc.types.Field(HideAssignmentGradesPayload, graphql_name='hideAssignmentGrades', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(HideAssignmentGradesInput), graphql_name='input', default=None)),
))
    )
    hide_assignment_grades_for_sections = sgqlc.types.Field(HideAssignmentGradesForSectionsPayload, graphql_name='hideAssignmentGradesForSections', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(HideAssignmentGradesForSectionsInput), graphql_name='input', default=None)),
))
    )
    import_outcomes = sgqlc.types.Field(ImportOutcomesPayload, graphql_name='importOutcomes', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(ImportOutcomesInput), graphql_name='input', default=None)),
))
    )
    mark_submission_comments_read = sgqlc.types.Field(MarkSubmissionCommentsReadPayload, graphql_name='markSubmissionCommentsRead', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(MarkSubmissionCommentsReadInput), graphql_name='input', default=None)),
))
    )
    move_outcome_links = sgqlc.types.Field(MoveOutcomeLinksPayload, graphql_name='moveOutcomeLinks', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(MoveOutcomeLinksInput), graphql_name='input', default=None)),
))
    )
    post_assignment_grades = sgqlc.types.Field('PostAssignmentGradesPayload', graphql_name='postAssignmentGrades', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(PostAssignmentGradesInput), graphql_name='input', default=None)),
))
    )
    post_assignment_grades_for_sections = sgqlc.types.Field('PostAssignmentGradesForSectionsPayload', graphql_name='postAssignmentGradesForSections', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(PostAssignmentGradesForSectionsInput), graphql_name='input', default=None)),
))
    )
    set_assignment_post_policy = sgqlc.types.Field('SetAssignmentPostPolicyPayload', graphql_name='setAssignmentPostPolicy', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(SetAssignmentPostPolicyInput), graphql_name='input', default=None)),
))
    )
    set_course_post_policy = sgqlc.types.Field('SetCoursePostPolicyPayload', graphql_name='setCoursePostPolicy', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(SetCoursePostPolicyInput), graphql_name='input', default=None)),
))
    )
    set_friendly_description = sgqlc.types.Field('SetFriendlyDescriptionPayload', graphql_name='setFriendlyDescription', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(SetFriendlyDescriptionInput), graphql_name='input', default=None)),
))
    )
    set_module_item_completion = sgqlc.types.Field('SetModuleItemCompletionPayload', graphql_name='setModuleItemCompletion', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(SetModuleItemCompletionInput), graphql_name='input', default=None)),
))
    )
    set_override_score = sgqlc.types.Field('SetOverrideScorePayload', graphql_name='setOverrideScore', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(SetOverrideScoreInput), graphql_name='input', default=None)),
))
    )
    set_override_status = sgqlc.types.Field('SetOverrideStatusPayload', graphql_name='setOverrideStatus', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(SetOverrideStatusInput), graphql_name='input', default=None)),
))
    )
    subscribe_to_discussion_topic = sgqlc.types.Field('SubscribeToDiscussionTopicPayload', graphql_name='subscribeToDiscussionTopic', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(SubscribeToDiscussionTopicInput), graphql_name='input', default=None)),
))
    )
    update_account_domain_lookup = sgqlc.types.Field('UpdateAccountDomainLookupPayload', graphql_name='updateAccountDomainLookup', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateAccountDomainLookupInput), graphql_name='input', default=None)),
))
    )
    update_assignment = sgqlc.types.Field('UpdateAssignmentPayload', graphql_name='updateAssignment', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateAssignmentInput), graphql_name='input', default=None)),
))
    )
    update_comment_bank_item = sgqlc.types.Field('UpdateCommentBankItemPayload', graphql_name='updateCommentBankItem', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateCommentBankItemInput), graphql_name='input', default=None)),
))
    )
    update_conversation_participants = sgqlc.types.Field('UpdateConversationParticipantsPayload', graphql_name='updateConversationParticipants', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateConversationParticipantsInput), graphql_name='input', default=None)),
))
    )
    update_discussion_entries_read_state = sgqlc.types.Field('UpdateDiscussionEntriesReadStatePayload', graphql_name='updateDiscussionEntriesReadState', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateDiscussionEntriesReadStateInput), graphql_name='input', default=None)),
))
    )
    update_discussion_entry = sgqlc.types.Field('UpdateDiscussionEntryPayload', graphql_name='updateDiscussionEntry', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateDiscussionEntryInput), graphql_name='input', default=None)),
))
    )
    update_discussion_entry_participant = sgqlc.types.Field('UpdateDiscussionEntryParticipantPayload', graphql_name='updateDiscussionEntryParticipant', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateDiscussionEntryParticipantInput), graphql_name='input', default=None)),
))
    )
    update_discussion_read_state = sgqlc.types.Field('UpdateDiscussionReadStatePayload', graphql_name='updateDiscussionReadState', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateDiscussionReadStateInput), graphql_name='input', default=None)),
))
    )
    update_discussion_thread_read_state = sgqlc.types.Field('UpdateDiscussionThreadReadStatePayload', graphql_name='updateDiscussionThreadReadState', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateDiscussionThreadReadStateInput), graphql_name='input', default=None)),
))
    )
    update_discussion_topic = sgqlc.types.Field('UpdateDiscussionTopicPayload', graphql_name='updateDiscussionTopic', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateDiscussionTopicInput), graphql_name='input', default=None)),
))
    )
    update_internal_setting = sgqlc.types.Field('UpdateInternalSettingPayload', graphql_name='updateInternalSetting', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateInternalSettingInput), graphql_name='input', default=None)),
))
    )
    update_isolated_view_deeply_nested_alert = sgqlc.types.Field('UpdateIsolatedViewDeeplyNestedAlertPayload', graphql_name='updateIsolatedViewDeeplyNestedAlert', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateIsolatedViewDeeplyNestedAlertInput), graphql_name='input', default=None)),
))
    )
    update_learning_outcome = sgqlc.types.Field('UpdateLearningOutcomePayload', graphql_name='updateLearningOutcome', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateLearningOutcomeInput), graphql_name='input', default=None)),
))
    )
    update_learning_outcome_group = sgqlc.types.Field('UpdateLearningOutcomeGroupPayload', graphql_name='updateLearningOutcomeGroup', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateLearningOutcomeGroupInput), graphql_name='input', default=None)),
))
    )
    update_notification_preferences = sgqlc.types.Field('UpdateNotificationPreferencesPayload', graphql_name='updateNotificationPreferences', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateNotificationPreferencesInput), graphql_name='input', default=None)),
))
    )
    update_outcome_calculation_method = sgqlc.types.Field('UpdateOutcomeCalculationMethodPayload', graphql_name='updateOutcomeCalculationMethod', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateOutcomeCalculationMethodInput), graphql_name='input', default=None)),
))
    )
    update_outcome_proficiency = sgqlc.types.Field('UpdateOutcomeProficiencyPayload', graphql_name='updateOutcomeProficiency', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateOutcomeProficiencyInput), graphql_name='input', default=None)),
))
    )
    update_rubric_archived_state = sgqlc.types.Field('UpdateRubricArchivedStatePayload', graphql_name='updateRubricArchivedState', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateRubricArchivedStateInput), graphql_name='input', default=None)),
))
    )
    update_submission_grade = sgqlc.types.Field('UpdateSubmissionsGradePayload', graphql_name='updateSubmissionGrade', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateSubmissionsGradeInput), graphql_name='input', default=None)),
))
    )
    update_submission_student_entered_score = sgqlc.types.Field('UpdateSubmissionStudentEnteredScorePayload', graphql_name='updateSubmissionStudentEnteredScore', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateSubmissionStudentEnteredScoreInput), graphql_name='input', default=None)),
))
    )
    update_submissions_read_state = sgqlc.types.Field('UpdateSubmissionsReadStatePayload', graphql_name='updateSubmissionsReadState', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateSubmissionsReadStateInput), graphql_name='input', default=None)),
))
    )
    update_user_discussions_splitscreen_view = sgqlc.types.Field('UpdateUserDiscussionsSplitscreenViewPayload', graphql_name='updateUserDiscussionsSplitscreenView', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateUserDiscussionsSplitscreenViewInput), graphql_name='input', default=None)),
))
    )
    upsert_custom_grade_status = sgqlc.types.Field('UpsertCustomGradeStatusPayload', graphql_name='upsertCustomGradeStatus', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpsertCustomGradeStatusInput), graphql_name='input', default=None)),
))
    )
    upsert_standard_grade_status = sgqlc.types.Field('UpsertStandardGradeStatusPayload', graphql_name='upsertStandardGradeStatus', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpsertStandardGradeStatusInput), graphql_name='input', default=None)),
))
    )


class MutationLog(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('asset_string', 'mutation_id', 'mutation_name', 'params', 'real_user', 'timestamp', 'user')
    asset_string = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assetString')
    mutation_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='mutationId')
    mutation_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='mutationName')
    params = sgqlc.types.Field(JSON, graphql_name='params')
    real_user = sgqlc.types.Field('User', graphql_name='realUser')
    timestamp = sgqlc.types.Field(DateTime, graphql_name='timestamp')
    user = sgqlc.types.Field('User', graphql_name='user')


class MutationLogConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('MutationLogEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of(MutationLog), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')


class MutationLogEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(MutationLog, graphql_name='node')


class Noop(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('_id',)
    _id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='_id')


class NotificationPreferences(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('channels', 'read_privacy_notice_date', 'send_observed_names_in_notifications', 'send_scores_in_emails')
    channels = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('CommunicationChannel')), graphql_name='channels', args=sgqlc.types.ArgDict((
        ('channel_id', sgqlc.types.Arg(ID, graphql_name='channelId', default=None)),
))
    )
    read_privacy_notice_date = sgqlc.types.Field(String, graphql_name='readPrivacyNoticeDate')
    send_observed_names_in_notifications = sgqlc.types.Field(Boolean, graphql_name='sendObservedNamesInNotifications')
    send_scores_in_emails = sgqlc.types.Field(Boolean, graphql_name='sendScoresInEmails', args=sgqlc.types.ArgDict((
        ('course_id', sgqlc.types.Arg(ID, graphql_name='courseId', default=None)),
))
    )


class PageInfo(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('end_cursor', 'has_next_page', 'has_previous_page', 'start_cursor')
    end_cursor = sgqlc.types.Field(String, graphql_name='endCursor')
    has_next_page = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hasNextPage')
    has_previous_page = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hasPreviousPage')
    start_cursor = sgqlc.types.Field(String, graphql_name='startCursor')


class PageViewAnalysis(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('level', 'max', 'total')
    level = sgqlc.types.Field(Int, graphql_name='level')
    max = sgqlc.types.Field(Int, graphql_name='max')
    total = sgqlc.types.Field(Int, graphql_name='total')


class PeerReviews(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('anonymous_reviews', 'automatic_reviews', 'count', 'due_at', 'enabled', 'intra_reviews')
    anonymous_reviews = sgqlc.types.Field(Boolean, graphql_name='anonymousReviews')
    automatic_reviews = sgqlc.types.Field(Boolean, graphql_name='automaticReviews')
    count = sgqlc.types.Field(Int, graphql_name='count')
    due_at = sgqlc.types.Field(DateTime, graphql_name='dueAt')
    enabled = sgqlc.types.Field(Boolean, graphql_name='enabled')
    intra_reviews = sgqlc.types.Field(Boolean, graphql_name='intraReviews')


class PostAssignmentGradesForSectionsPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('assignment', 'errors', 'progress', 'sections')
    assignment = sgqlc.types.Field('Assignment', graphql_name='assignment')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    progress = sgqlc.types.Field('Progress', graphql_name='progress')
    sections = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('Section')), graphql_name='sections')


class PostAssignmentGradesPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('assignment', 'errors', 'progress', 'sections')
    assignment = sgqlc.types.Field('Assignment', graphql_name='assignment')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    progress = sgqlc.types.Field('Progress', graphql_name='progress')
    sections = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('Section')), graphql_name='sections')


class PostPolicyConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('PostPolicyEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('PostPolicy'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')


class PostPolicyEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('PostPolicy', graphql_name='node')


class ProficiencyRatingConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('ProficiencyRatingEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('ProficiencyRating'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')


class ProficiencyRatingEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('ProficiencyRating', graphql_name='node')


class Query(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('account', 'all_courses', 'assignment', 'assignment_group', 'audit_logs', 'course', 'internal_setting', 'internal_settings', 'learning_outcome', 'learning_outcome_group', 'legacy_node', 'module_item', 'node', 'outcome_calculation_method', 'outcome_proficiency', 'submission', 'term')
    account = sgqlc.types.Field('Account', graphql_name='account', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(ID, graphql_name='id', default=None)),
        ('sis_id', sgqlc.types.Arg(String, graphql_name='sisId', default=None)),
))
    )
    all_courses = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('Course')), graphql_name='allCourses')
    assignment = sgqlc.types.Field('Assignment', graphql_name='assignment', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(ID, graphql_name='id', default=None)),
        ('sis_id', sgqlc.types.Arg(String, graphql_name='sisId', default=None)),
))
    )
    assignment_group = sgqlc.types.Field('AssignmentGroup', graphql_name='assignmentGroup', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(ID, graphql_name='id', default=None)),
        ('sis_id', sgqlc.types.Arg(String, graphql_name='sisId', default=None)),
))
    )
    audit_logs = sgqlc.types.Field(AuditLogs, graphql_name='auditLogs')
    course = sgqlc.types.Field('Course', graphql_name='course', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(ID, graphql_name='id', default=None)),
        ('sis_id', sgqlc.types.Arg(String, graphql_name='sisId', default=None)),
))
    )
    internal_setting = sgqlc.types.Field('InternalSetting', graphql_name='internalSetting', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(ID, graphql_name='id', default=None)),
        ('name', sgqlc.types.Arg(String, graphql_name='name', default=None)),
))
    )
    internal_settings = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('InternalSetting')), graphql_name='internalSettings')
    learning_outcome = sgqlc.types.Field('LearningOutcome', graphql_name='learningOutcome', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    learning_outcome_group = sgqlc.types.Field('LearningOutcomeGroup', graphql_name='learningOutcomeGroup', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    legacy_node = sgqlc.types.Field(Node, graphql_name='legacyNode', args=sgqlc.types.ArgDict((
        ('_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='_id', default=None)),
        ('type', sgqlc.types.Arg(sgqlc.types.non_null(NodeType), graphql_name='type', default=None)),
))
    )
    module_item = sgqlc.types.Field('ModuleItem', graphql_name='moduleItem', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    node = sgqlc.types.Field(Node, graphql_name='node', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    outcome_calculation_method = sgqlc.types.Field('OutcomeCalculationMethod', graphql_name='outcomeCalculationMethod', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    outcome_proficiency = sgqlc.types.Field('OutcomeProficiency', graphql_name='outcomeProficiency', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    submission = sgqlc.types.Field('Submission', graphql_name='submission', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    term = sgqlc.types.Field('Term', graphql_name='term', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(ID, graphql_name='id', default=None)),
        ('sis_id', sgqlc.types.Arg(String, graphql_name='sisId', default=None)),
))
    )


class QuizItem(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('_id', 'title')
    _id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='_id')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')


class Recipients(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('contexts_connection', 'send_messages_all', 'users_connection')
    contexts_connection = sgqlc.types.Field(MessageableContextConnection, graphql_name='contextsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    send_messages_all = sgqlc.types.Field(Boolean, graphql_name='sendMessagesAll')
    users_connection = sgqlc.types.Field(MessageableUserConnection, graphql_name='usersConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )


class RubricAssessmentConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('RubricAssessmentEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('RubricAssessment'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')


class RubricAssessmentEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('RubricAssessment', graphql_name='node')


class RubricAssessmentRating(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('_id', 'artifact_attempt', 'comments', 'comments_html', 'criterion', 'description', 'outcome', 'points', 'rubric_assessment_id')
    _id = sgqlc.types.Field(ID, graphql_name='_id')
    artifact_attempt = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='artifactAttempt')
    comments = sgqlc.types.Field(String, graphql_name='comments')
    comments_html = sgqlc.types.Field(String, graphql_name='commentsHtml')
    criterion = sgqlc.types.Field('RubricCriterion', graphql_name='criterion')
    description = sgqlc.types.Field(String, graphql_name='description')
    outcome = sgqlc.types.Field('LearningOutcome', graphql_name='outcome')
    points = sgqlc.types.Field(Float, graphql_name='points')
    rubric_assessment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='rubricAssessmentId')


class RubricConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('RubricEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('Rubric'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')


class RubricEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('Rubric', graphql_name='node')


class SectionConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('SectionEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('Section'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')


class SectionEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('Section', graphql_name='node')


class SetAssignmentPostPolicyPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'post_policy')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    post_policy = sgqlc.types.Field('PostPolicy', graphql_name='postPolicy')


class SetCoursePostPolicyPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'post_policy')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    post_policy = sgqlc.types.Field('PostPolicy', graphql_name='postPolicy')


class SetFriendlyDescriptionPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'outcome_friendly_description')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    outcome_friendly_description = sgqlc.types.Field('OutcomeFriendlyDescriptionType', graphql_name='outcomeFriendlyDescription')


class SetModuleItemCompletionPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'module_item')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    module_item = sgqlc.types.Field(sgqlc.types.non_null('ModuleItem'), graphql_name='moduleItem')


class SetOverrideScorePayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'grades')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    grades = sgqlc.types.Field(Grades, graphql_name='grades')


class SetOverrideStatusPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'grades')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    grades = sgqlc.types.Field(Grades, graphql_name='grades')


class StandardGradeStatusConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('StandardGradeStatusEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('StandardGradeStatus'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')


class StandardGradeStatusEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('StandardGradeStatus', graphql_name='node')


class StudentSummaryAnalytics(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('page_views', 'participations', 'tardiness_breakdown')
    page_views = sgqlc.types.Field(PageViewAnalysis, graphql_name='pageViews')
    participations = sgqlc.types.Field(PageViewAnalysis, graphql_name='participations')
    tardiness_breakdown = sgqlc.types.Field('TardinessBreakdown', graphql_name='tardinessBreakdown')


class SubmissionCommentConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('SubmissionCommentEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('SubmissionComment'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')


class SubmissionCommentEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('SubmissionComment', graphql_name='node')


class SubmissionConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('SubmissionEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('Submission'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')


class SubmissionEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('Submission', graphql_name='node')


class SubmissionHistoryConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('SubmissionHistoryEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('SubmissionHistory'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')


class SubmissionHistoryEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('SubmissionHistory', graphql_name='node')


class SubscribeToDiscussionTopicPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('discussion_topic', 'errors')
    discussion_topic = sgqlc.types.Field(sgqlc.types.non_null('Discussion'), graphql_name='discussionTopic')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class TardinessBreakdown(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('late', 'missing', 'on_time', 'total')
    late = sgqlc.types.Field(Float, graphql_name='late')
    missing = sgqlc.types.Field(Float, graphql_name='missing')
    on_time = sgqlc.types.Field(Float, graphql_name='onTime')
    total = sgqlc.types.Field(Int, graphql_name='total')


class TurnitinData(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('report_url', 'score', 'state', 'status', 'target')
    report_url = sgqlc.types.Field(String, graphql_name='reportUrl')
    score = sgqlc.types.Field(Float, graphql_name='score')
    state = sgqlc.types.Field(String, graphql_name='state')
    status = sgqlc.types.Field(String, graphql_name='status')
    target = sgqlc.types.Field(sgqlc.types.non_null('TurnitinContext'), graphql_name='target')


class UpdateAccountDomainLookupPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('account_domain_lookup', 'errors')
    account_domain_lookup = sgqlc.types.Field('AccountDomainLookup', graphql_name='accountDomainLookup')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class UpdateAssignmentPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('assignment', 'errors')
    assignment = sgqlc.types.Field('Assignment', graphql_name='assignment')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class UpdateCommentBankItemPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('comment_bank_item', 'errors')
    comment_bank_item = sgqlc.types.Field('CommentBankItem', graphql_name='commentBankItem')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class UpdateConversationParticipantsPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('conversation_participants', 'errors')
    conversation_participants = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ConversationParticipant)), graphql_name='conversationParticipants')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class UpdateDiscussionEntriesReadStatePayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('discussion_entries', 'errors')
    discussion_entries = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('DiscussionEntry')), graphql_name='discussionEntries')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class UpdateDiscussionEntryParticipantPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('discussion_entry', 'errors')
    discussion_entry = sgqlc.types.Field(sgqlc.types.non_null('DiscussionEntry'), graphql_name='discussionEntry')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class UpdateDiscussionEntryPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('discussion_entry', 'errors')
    discussion_entry = sgqlc.types.Field('DiscussionEntry', graphql_name='discussionEntry')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class UpdateDiscussionReadStatePayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('discussion_topic', 'errors')
    discussion_topic = sgqlc.types.Field(sgqlc.types.non_null('Discussion'), graphql_name='discussionTopic')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class UpdateDiscussionThreadReadStatePayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('discussion_entry', 'errors')
    discussion_entry = sgqlc.types.Field(sgqlc.types.non_null('DiscussionEntry'), graphql_name='discussionEntry')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class UpdateDiscussionTopicPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('discussion_topic', 'errors')
    discussion_topic = sgqlc.types.Field(sgqlc.types.non_null('Discussion'), graphql_name='discussionTopic')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class UpdateInternalSettingPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'internal_setting')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    internal_setting = sgqlc.types.Field(sgqlc.types.non_null('InternalSetting'), graphql_name='internalSetting')


class UpdateIsolatedViewDeeplyNestedAlertPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'user')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    user = sgqlc.types.Field(sgqlc.types.non_null('User'), graphql_name='user')


class UpdateLearningOutcomeGroupPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'learning_outcome_group')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    learning_outcome_group = sgqlc.types.Field('LearningOutcomeGroup', graphql_name='learningOutcomeGroup')


class UpdateLearningOutcomePayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'learning_outcome')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    learning_outcome = sgqlc.types.Field('LearningOutcome', graphql_name='learningOutcome')


class UpdateNotificationPreferencesPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'user')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    user = sgqlc.types.Field('User', graphql_name='user')


class UpdateOutcomeCalculationMethodPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'outcome_calculation_method')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    outcome_calculation_method = sgqlc.types.Field('OutcomeCalculationMethod', graphql_name='outcomeCalculationMethod')


class UpdateOutcomeProficiencyPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'outcome_proficiency')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    outcome_proficiency = sgqlc.types.Field('OutcomeProficiency', graphql_name='outcomeProficiency')


class UpdateRubricArchivedStatePayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'rubric')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    rubric = sgqlc.types.Field('Rubric', graphql_name='rubric')


class UpdateSubmissionStudentEnteredScorePayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'submission')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    submission = sgqlc.types.Field('Submission', graphql_name='submission')


class UpdateSubmissionsGradePayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'submission')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    submission = sgqlc.types.Field('Submission', graphql_name='submission')


class UpdateSubmissionsReadStatePayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'submissions')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    submissions = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('Submission')), graphql_name='submissions')


class UpdateUserDiscussionsSplitscreenViewPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'user')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    user = sgqlc.types.Field(sgqlc.types.non_null('User'), graphql_name='user')


class UpsertCustomGradeStatusPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('custom_grade_status', 'errors')
    custom_grade_status = sgqlc.types.Field('CustomGradeStatus', graphql_name='customGradeStatus')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')


class UpsertStandardGradeStatusPayload(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('errors', 'standard_grade_status')
    errors = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ValidationError')), graphql_name='errors')
    standard_grade_status = sgqlc.types.Field('StandardGradeStatus', graphql_name='standardGradeStatus')


class UserConnection(sgqlc.types.relay.Connection):
    __schema__ = canvas_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('UserEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of('User'), graphql_name='nodes')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')


class UserEdge(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field('User', graphql_name='node')


class ValidationError(sgqlc.types.Type):
    __schema__ = canvas_schema
    __field_names__ = ('attribute', 'message')
    attribute = sgqlc.types.Field(String, graphql_name='attribute')
    message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='message')


class Account(sgqlc.types.Type, Node, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('account_domain_lookups', 'account_domains', 'courses_connection', 'custom_grade_statuses_connection', 'name', 'outcome_calculation_method', 'outcome_proficiency', 'parent_accounts_connection', 'proficiency_ratings_connection', 'root_outcome_group', 'rubrics_connection', 'sis_id', 'standard_grade_statuses_connection', 'sub_accounts_connection')
    account_domain_lookups = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('AccountDomainLookup')), graphql_name='accountDomainLookups')
    account_domains = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('AccountDomain')), graphql_name='accountDomains')
    courses_connection = sgqlc.types.Field(CourseConnection, graphql_name='coursesConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    custom_grade_statuses_connection = sgqlc.types.Field(CustomGradeStatusConnection, graphql_name='customGradeStatusesConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    name = sgqlc.types.Field(String, graphql_name='name')
    outcome_calculation_method = sgqlc.types.Field('OutcomeCalculationMethod', graphql_name='outcomeCalculationMethod')
    outcome_proficiency = sgqlc.types.Field('OutcomeProficiency', graphql_name='outcomeProficiency')
    parent_accounts_connection = sgqlc.types.Field(sgqlc.types.non_null(AccountConnection), graphql_name='parentAccountsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    proficiency_ratings_connection = sgqlc.types.Field(ProficiencyRatingConnection, graphql_name='proficiencyRatingsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    root_outcome_group = sgqlc.types.Field(sgqlc.types.non_null('LearningOutcomeGroup'), graphql_name='rootOutcomeGroup')
    rubrics_connection = sgqlc.types.Field(RubricConnection, graphql_name='rubricsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    sis_id = sgqlc.types.Field(String, graphql_name='sisId')
    standard_grade_statuses_connection = sgqlc.types.Field(StandardGradeStatusConnection, graphql_name='standardGradeStatusesConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    sub_accounts_connection = sgqlc.types.Field(AccountConnection, graphql_name='subAccountsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )


class AccountDomain(sgqlc.types.Type, LegacyIDInterface, Timestamped):
    __schema__ = canvas_schema
    __field_names__ = ('host',)
    host = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='host')


class AccountDomainLookup(sgqlc.types.Type, LegacyIDInterface, Timestamped):
    __schema__ = canvas_schema
    __field_names__ = ('account_domain', 'authentication_provider', 'name')
    account_domain = sgqlc.types.Field(AccountDomain, graphql_name='accountDomain')
    authentication_provider = sgqlc.types.Field(String, graphql_name='authenticationProvider')
    name = sgqlc.types.Field(String, graphql_name='name')


class AssessmentRequest(sgqlc.types.Type, Timestamped, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('anonymized_user', 'anonymous_id', 'asset_id', 'asset_submission_type', 'available', 'user', 'workflow_state')
    anonymized_user = sgqlc.types.Field('User', graphql_name='anonymizedUser')
    anonymous_id = sgqlc.types.Field(String, graphql_name='anonymousId')
    asset_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='assetId')
    asset_submission_type = sgqlc.types.Field(String, graphql_name='assetSubmissionType')
    available = sgqlc.types.Field(Boolean, graphql_name='available')
    user = sgqlc.types.Field(sgqlc.types.non_null('User'), graphql_name='user')
    workflow_state = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='workflowState')


class Assignment(sgqlc.types.Type, Node, Timestamped, ModuleItemInterface, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('allow_google_docs_submission', 'allowed_attempts', 'allowed_extensions', 'anonymize_students', 'anonymous_grading', 'anonymous_instructor_annotations', 'assessment_requests_for_current_user', 'assignment_group', 'assignment_group_id', 'assignment_overrides', 'can_duplicate', 'can_unpublish', 'checkpointed', 'checkpoints', 'course', 'course_id', 'description', 'discussion', 'due_at', 'due_date_required', 'expects_external_submission', 'expects_submission', 'grade_group_students_individually', 'grades_published', 'grading_period_id', 'grading_standard', 'grading_type', 'group_category_id', 'group_set', 'group_submissions_connection', 'has_submitted_submissions', 'html_url', 'in_closed_grading_period', 'lock_at', 'lock_info', 'moderated_grading', 'moderated_grading_enabled', 'name', 'needs_grading_count', 'non_digital_submission', 'omit_from_final_grade', 'only_visible_to_overrides', 'originality_report_visibility', 'peer_reviews', 'points_possible', 'position', 'post_manually', 'post_policy', 'post_to_sis', 'published', 'quiz', 'restrict_quantitative_data', 'rubric', 'rubric_association', 'score_statistic', 'sis_id', 'state', 'submission_types', 'submissions_connection', 'submissions_downloads', 'time_zone_edited', 'unlock_at')
    allow_google_docs_submission = sgqlc.types.Field(Boolean, graphql_name='allowGoogleDocsSubmission')
    allowed_attempts = sgqlc.types.Field(Int, graphql_name='allowedAttempts')
    allowed_extensions = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='allowedExtensions')
    anonymize_students = sgqlc.types.Field(Boolean, graphql_name='anonymizeStudents')
    anonymous_grading = sgqlc.types.Field(Boolean, graphql_name='anonymousGrading')
    anonymous_instructor_annotations = sgqlc.types.Field(Boolean, graphql_name='anonymousInstructorAnnotations')
    assessment_requests_for_current_user = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(AssessmentRequest)), graphql_name='assessmentRequestsForCurrentUser')
    assignment_group = sgqlc.types.Field('AssignmentGroup', graphql_name='assignmentGroup')
    assignment_group_id = sgqlc.types.Field(ID, graphql_name='assignmentGroupId')
    assignment_overrides = sgqlc.types.Field(AssignmentOverrideConnection, graphql_name='assignmentOverrides', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    can_duplicate = sgqlc.types.Field(Boolean, graphql_name='canDuplicate')
    can_unpublish = sgqlc.types.Field(Boolean, graphql_name='canUnpublish')
    checkpointed = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='checkpointed')
    checkpoints = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Checkpoint)), graphql_name='checkpoints')
    course = sgqlc.types.Field('Course', graphql_name='course')
    course_id = sgqlc.types.Field(ID, graphql_name='courseId')
    description = sgqlc.types.Field(String, graphql_name='description')
    discussion = sgqlc.types.Field('Discussion', graphql_name='discussion')
    due_at = sgqlc.types.Field(DateTime, graphql_name='dueAt', args=sgqlc.types.ArgDict((
        ('apply_overrides', sgqlc.types.Arg(Boolean, graphql_name='applyOverrides', default=True)),
))
    )
    due_date_required = sgqlc.types.Field(Boolean, graphql_name='dueDateRequired')
    expects_external_submission = sgqlc.types.Field(Boolean, graphql_name='expectsExternalSubmission')
    expects_submission = sgqlc.types.Field(Boolean, graphql_name='expectsSubmission')
    grade_group_students_individually = sgqlc.types.Field(Boolean, graphql_name='gradeGroupStudentsIndividually')
    grades_published = sgqlc.types.Field(Boolean, graphql_name='gradesPublished')
    grading_period_id = sgqlc.types.Field(String, graphql_name='gradingPeriodId')
    grading_standard = sgqlc.types.Field(GradingStandard, graphql_name='gradingStandard')
    grading_type = sgqlc.types.Field(GradingType, graphql_name='gradingType')
    group_category_id = sgqlc.types.Field(Int, graphql_name='groupCategoryId')
    group_set = sgqlc.types.Field('GroupSet', graphql_name='groupSet')
    group_submissions_connection = sgqlc.types.Field(SubmissionConnection, graphql_name='groupSubmissionsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
        ('filter', sgqlc.types.Arg(SubmissionSearchFilterInput, graphql_name='filter', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(SubmissionSearchOrder)), graphql_name='orderBy', default=None)),
))
    )
    has_submitted_submissions = sgqlc.types.Field(Boolean, graphql_name='hasSubmittedSubmissions')
    html_url = sgqlc.types.Field(URL, graphql_name='htmlUrl')
    in_closed_grading_period = sgqlc.types.Field(Boolean, graphql_name='inClosedGradingPeriod')
    lock_at = sgqlc.types.Field(DateTime, graphql_name='lockAt', args=sgqlc.types.ArgDict((
        ('apply_overrides', sgqlc.types.Arg(Boolean, graphql_name='applyOverrides', default=True)),
))
    )
    lock_info = sgqlc.types.Field(LockInfo, graphql_name='lockInfo')
    moderated_grading = sgqlc.types.Field(ModeratedGrading, graphql_name='moderatedGrading')
    moderated_grading_enabled = sgqlc.types.Field(Boolean, graphql_name='moderatedGradingEnabled')
    name = sgqlc.types.Field(String, graphql_name='name')
    needs_grading_count = sgqlc.types.Field(Int, graphql_name='needsGradingCount')
    non_digital_submission = sgqlc.types.Field(Boolean, graphql_name='nonDigitalSubmission')
    omit_from_final_grade = sgqlc.types.Field(Boolean, graphql_name='omitFromFinalGrade')
    only_visible_to_overrides = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='onlyVisibleToOverrides')
    originality_report_visibility = sgqlc.types.Field(String, graphql_name='originalityReportVisibility')
    peer_reviews = sgqlc.types.Field(PeerReviews, graphql_name='peerReviews')
    points_possible = sgqlc.types.Field(Float, graphql_name='pointsPossible')
    position = sgqlc.types.Field(Int, graphql_name='position')
    post_manually = sgqlc.types.Field(Boolean, graphql_name='postManually')
    post_policy = sgqlc.types.Field('PostPolicy', graphql_name='postPolicy')
    post_to_sis = sgqlc.types.Field(Boolean, graphql_name='postToSis')
    published = sgqlc.types.Field(Boolean, graphql_name='published')
    quiz = sgqlc.types.Field('Quiz', graphql_name='quiz')
    restrict_quantitative_data = sgqlc.types.Field(Boolean, graphql_name='restrictQuantitativeData', args=sgqlc.types.ArgDict((
        ('check_extra_permissions', sgqlc.types.Arg(Boolean, graphql_name='checkExtraPermissions', default=None)),
))
    )
    rubric = sgqlc.types.Field('Rubric', graphql_name='rubric')
    rubric_association = sgqlc.types.Field('RubricAssociation', graphql_name='rubricAssociation')
    score_statistic = sgqlc.types.Field(AssignmentScoreStatistic, graphql_name='scoreStatistic')
    sis_id = sgqlc.types.Field(String, graphql_name='sisId')
    state = sgqlc.types.Field(sgqlc.types.non_null(AssignmentState), graphql_name='state')
    submission_types = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(SubmissionType)), graphql_name='submissionTypes')
    submissions_connection = sgqlc.types.Field(SubmissionConnection, graphql_name='submissionsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
        ('filter', sgqlc.types.Arg(SubmissionSearchFilterInput, graphql_name='filter', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(SubmissionSearchOrder)), graphql_name='orderBy', default=None)),
))
    )
    submissions_downloads = sgqlc.types.Field(Int, graphql_name='submissionsDownloads')
    time_zone_edited = sgqlc.types.Field(String, graphql_name='timeZoneEdited')
    unlock_at = sgqlc.types.Field(DateTime, graphql_name='unlockAt', args=sgqlc.types.ArgDict((
        ('apply_overrides', sgqlc.types.Arg(Boolean, graphql_name='applyOverrides', default=True)),
))
    )


class AssignmentGroup(sgqlc.types.Type, Node, Timestamped, LegacyIDInterface, AssignmentsConnectionInterface):
    __schema__ = canvas_schema
    __field_names__ = ('grades_connection', 'group_weight', 'name', 'position', 'rules', 'sis_id', 'state')
    grades_connection = sgqlc.types.Field(GradesConnection, graphql_name='gradesConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
        ('filter', sgqlc.types.Arg(GradesEnrollmentFilter, graphql_name='filter', default=None)),
))
    )
    group_weight = sgqlc.types.Field(Float, graphql_name='groupWeight')
    name = sgqlc.types.Field(String, graphql_name='name')
    position = sgqlc.types.Field(Int, graphql_name='position')
    rules = sgqlc.types.Field(AssignmentGroupRules, graphql_name='rules')
    sis_id = sgqlc.types.Field(String, graphql_name='sisId')
    state = sgqlc.types.Field(sgqlc.types.non_null(AssignmentGroupState), graphql_name='state')


class AssignmentOverride(sgqlc.types.Type, Node, Timestamped, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('all_day', 'assignment', 'due_at', 'lock_at', 'set', 'title', 'unlock_at')
    all_day = sgqlc.types.Field(Boolean, graphql_name='allDay')
    assignment = sgqlc.types.Field(Assignment, graphql_name='assignment')
    due_at = sgqlc.types.Field(DateTime, graphql_name='dueAt')
    lock_at = sgqlc.types.Field(DateTime, graphql_name='lockAt')
    set = sgqlc.types.Field('AssignmentOverrideSet', graphql_name='set')
    title = sgqlc.types.Field(String, graphql_name='title')
    unlock_at = sgqlc.types.Field(DateTime, graphql_name='unlockAt')


class CommentBankItem(sgqlc.types.Type, Node, LegacyIDInterface, Timestamped):
    __schema__ = canvas_schema
    __field_names__ = ('comment', 'course_id', 'user_id')
    comment = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='comment')
    course_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='courseId')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='userId')


class CommunicationChannel(sgqlc.types.Type, Node, Timestamped, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('notification_policies', 'notification_policy_overrides', 'path', 'path_type')
    notification_policies = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('NotificationPolicy')), graphql_name='notificationPolicies', args=sgqlc.types.ArgDict((
        ('context_type', sgqlc.types.Arg(NotificationPreferencesContextType, graphql_name='contextType', default=None)),
))
    )
    notification_policy_overrides = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('NotificationPolicy')), graphql_name='notificationPolicyOverrides', args=sgqlc.types.ArgDict((
        ('account_id', sgqlc.types.Arg(ID, graphql_name='accountId', default=None)),
        ('course_id', sgqlc.types.Arg(ID, graphql_name='courseId', default=None)),
        ('context_type', sgqlc.types.Arg(sgqlc.types.non_null(NotificationPreferencesContextType), graphql_name='contextType', default=None)),
))
    )
    path = sgqlc.types.Field(String, graphql_name='path')
    path_type = sgqlc.types.Field(String, graphql_name='pathType')


class ContentTag(sgqlc.types.Type, Node, LegacyIDInterface, Timestamped):
    __schema__ = canvas_schema
    __field_names__ = ('can_unlink', 'cursor', 'group', 'node')
    can_unlink = sgqlc.types.Field(Boolean, graphql_name='canUnlink')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    group = sgqlc.types.Field('LearningOutcomeGroup', graphql_name='group')
    node = sgqlc.types.Field('ContentTagContent', graphql_name='node')


class Conversation(sgqlc.types.Type, Node):
    __schema__ = canvas_schema
    __field_names__ = ('_id', 'can_reply', 'context_id', 'context_name', 'context_type', 'conversation_messages_connection', 'conversation_messages_count', 'conversation_participants_connection', 'is_private', 'subject', 'updated_at')
    _id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='_id')
    can_reply = sgqlc.types.Field(Boolean, graphql_name='canReply')
    context_id = sgqlc.types.Field(ID, graphql_name='contextId')
    context_name = sgqlc.types.Field(String, graphql_name='contextName')
    context_type = sgqlc.types.Field(String, graphql_name='contextType')
    conversation_messages_connection = sgqlc.types.Field(ConversationMessageConnection, graphql_name='conversationMessagesConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
        ('participants', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='participants', default=None)),
        ('created_before', sgqlc.types.Arg(DateTime, graphql_name='createdBefore', default=None)),
))
    )
    conversation_messages_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='conversationMessagesCount')
    conversation_participants_connection = sgqlc.types.Field(ConversationParticipantConnection, graphql_name='conversationParticipantsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    is_private = sgqlc.types.Field(Boolean, graphql_name='isPrivate')
    subject = sgqlc.types.Field(String, graphql_name='subject')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')


class Course(sgqlc.types.Type, AssetString, Node, Timestamped, LegacyIDInterface, AssignmentsConnectionInterface):
    __schema__ = canvas_schema
    __field_names__ = ('account', 'allow_final_grade_override', 'apply_group_weights', 'assignment_groups_connection', 'assignment_post_policies', 'course_code', 'course_nickname', 'enrollments_connection', 'external_tools_connection', 'grading_periods_connection', 'grading_standard', 'group_sets_connection', 'groups_connection', 'image_url', 'modules_connection', 'name', 'outcome_alignment_stats', 'outcome_calculation_method', 'outcome_proficiency', 'permissions', 'post_policy', 'relevant_grading_period_group', 'root_outcome_group', 'rubrics_connection', 'sections_connection', 'sis_id', 'state', 'submissions_connection', 'syllabus_body', 'term', 'users_connection')
    account = sgqlc.types.Field(Account, graphql_name='account')
    allow_final_grade_override = sgqlc.types.Field(Boolean, graphql_name='allowFinalGradeOverride')
    apply_group_weights = sgqlc.types.Field(Boolean, graphql_name='applyGroupWeights')
    assignment_groups_connection = sgqlc.types.Field(AssignmentGroupConnection, graphql_name='assignmentGroupsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    assignment_post_policies = sgqlc.types.Field(PostPolicyConnection, graphql_name='assignmentPostPolicies', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    course_code = sgqlc.types.Field(String, graphql_name='courseCode')
    course_nickname = sgqlc.types.Field(String, graphql_name='courseNickname')
    enrollments_connection = sgqlc.types.Field(EnrollmentConnection, graphql_name='enrollmentsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
        ('filter', sgqlc.types.Arg(EnrollmentFilterInput, graphql_name='filter', default=None)),
))
    )
    external_tools_connection = sgqlc.types.Field(ExternalToolConnection, graphql_name='externalToolsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
        ('filter', sgqlc.types.Arg(ExternalToolFilterInput, graphql_name='filter', default={})),
))
    )
    grading_periods_connection = sgqlc.types.Field(GradingPeriodConnection, graphql_name='gradingPeriodsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    grading_standard = sgqlc.types.Field(GradingStandard, graphql_name='gradingStandard')
    group_sets_connection = sgqlc.types.Field(GroupSetConnection, graphql_name='groupSetsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    groups_connection = sgqlc.types.Field(GroupConnection, graphql_name='groupsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    image_url = sgqlc.types.Field(URL, graphql_name='imageUrl')
    modules_connection = sgqlc.types.Field(ModuleConnection, graphql_name='modulesConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    outcome_alignment_stats = sgqlc.types.Field(CourseOutcomeAlignmentStats, graphql_name='outcomeAlignmentStats')
    outcome_calculation_method = sgqlc.types.Field('OutcomeCalculationMethod', graphql_name='outcomeCalculationMethod')
    outcome_proficiency = sgqlc.types.Field('OutcomeProficiency', graphql_name='outcomeProficiency')
    permissions = sgqlc.types.Field(CoursePermissions, graphql_name='permissions')
    post_policy = sgqlc.types.Field('PostPolicy', graphql_name='postPolicy')
    relevant_grading_period_group = sgqlc.types.Field('GradingPeriodGroup', graphql_name='relevantGradingPeriodGroup')
    root_outcome_group = sgqlc.types.Field(sgqlc.types.non_null('LearningOutcomeGroup'), graphql_name='rootOutcomeGroup')
    rubrics_connection = sgqlc.types.Field(RubricConnection, graphql_name='rubricsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    sections_connection = sgqlc.types.Field(SectionConnection, graphql_name='sectionsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    sis_id = sgqlc.types.Field(String, graphql_name='sisId')
    state = sgqlc.types.Field(sgqlc.types.non_null(CourseWorkflowState), graphql_name='state')
    submissions_connection = sgqlc.types.Field(SubmissionConnection, graphql_name='submissionsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
        ('student_ids', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='studentIds', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(SubmissionOrderCriteria)), graphql_name='orderBy', default=None)),
        ('filter', sgqlc.types.Arg(SubmissionFilterInput, graphql_name='filter', default=None)),
))
    )
    syllabus_body = sgqlc.types.Field(String, graphql_name='syllabusBody')
    term = sgqlc.types.Field('Term', graphql_name='term')
    users_connection = sgqlc.types.Field(UserConnection, graphql_name='usersConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
        ('user_ids', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='userIds', default=None)),
        ('filter', sgqlc.types.Arg(CourseUsersFilter, graphql_name='filter', default=None)),
))
    )


class CustomGradeStatus(sgqlc.types.Type, Node, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('color', 'name')
    color = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='color')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')


class Discussion(sgqlc.types.Type, Node, Timestamped, ModuleItemInterface, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('allow_rating', 'anonymous_author', 'anonymous_state', 'assignment', 'attachment', 'author', 'available_for_user', 'can_reply_anonymously', 'can_unpublish', 'child_topics', 'context_id', 'context_name', 'context_type', 'course_sections', 'delayed_post_at', 'discussion_entries_connection', 'discussion_entry_drafts_connection', 'discussion_type', 'editor', 'entries_total_pages', 'entry_counts', 'group_set', 'initial_post_required_for_current_user', 'is_announcement', 'is_anonymous_author', 'is_section_specific', 'last_reply_at', 'lock_at', 'locked', 'mentionable_users_connection', 'message', 'only_graders_can_rate', 'permissions', 'podcast_enabled', 'podcast_has_student_posts', 'position', 'posted_at', 'published', 'require_initial_post', 'root_entries_total_pages', 'root_topic', 'search_entry_count', 'sort_by_rating', 'subscribed', 'title', 'todo_date', 'user_count')
    allow_rating = sgqlc.types.Field(Boolean, graphql_name='allowRating')
    anonymous_author = sgqlc.types.Field(AnonymousUser, graphql_name='anonymousAuthor')
    anonymous_state = sgqlc.types.Field(String, graphql_name='anonymousState')
    assignment = sgqlc.types.Field(Assignment, graphql_name='assignment')
    attachment = sgqlc.types.Field('File', graphql_name='attachment')
    author = sgqlc.types.Field('User', graphql_name='author', args=sgqlc.types.ArgDict((
        ('course_id', sgqlc.types.Arg(String, graphql_name='courseId', default=None)),
        ('role_types', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='roleTypes', default=None)),
        ('built_in_only', sgqlc.types.Arg(Boolean, graphql_name='builtInOnly', default=None)),
))
    )
    available_for_user = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='availableForUser')
    can_reply_anonymously = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='canReplyAnonymously')
    can_unpublish = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='canUnpublish')
    child_topics = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('Discussion')), graphql_name='childTopics')
    context_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contextId')
    context_name = sgqlc.types.Field(String, graphql_name='contextName')
    context_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='contextType')
    course_sections = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Section'))), graphql_name='courseSections')
    delayed_post_at = sgqlc.types.Field(DateTime, graphql_name='delayedPostAt')
    discussion_entries_connection = sgqlc.types.Field(DiscussionEntryConnection, graphql_name='discussionEntriesConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
        ('search_term', sgqlc.types.Arg(String, graphql_name='searchTerm', default=None)),
        ('filter', sgqlc.types.Arg(DiscussionFilterType, graphql_name='filter', default=None)),
        ('sort_order', sgqlc.types.Arg(DiscussionSortOrderType, graphql_name='sortOrder', default=None)),
        ('root_entries', sgqlc.types.Arg(Boolean, graphql_name='rootEntries', default=None)),
        ('user_search_id', sgqlc.types.Arg(String, graphql_name='userSearchId', default=None)),
        ('unread_before', sgqlc.types.Arg(String, graphql_name='unreadBefore', default=None)),
))
    )
    discussion_entry_drafts_connection = sgqlc.types.Field(DiscussionEntryDraftConnection, graphql_name='discussionEntryDraftsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    discussion_type = sgqlc.types.Field(String, graphql_name='discussionType')
    editor = sgqlc.types.Field('User', graphql_name='editor', args=sgqlc.types.ArgDict((
        ('course_id', sgqlc.types.Arg(String, graphql_name='courseId', default=None)),
        ('role_types', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='roleTypes', default=None)),
        ('built_in_only', sgqlc.types.Arg(Boolean, graphql_name='builtInOnly', default=None)),
))
    )
    entries_total_pages = sgqlc.types.Field(Int, graphql_name='entriesTotalPages', args=sgqlc.types.ArgDict((
        ('per_page', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='perPage', default=None)),
        ('search_term', sgqlc.types.Arg(String, graphql_name='searchTerm', default=None)),
        ('filter', sgqlc.types.Arg(DiscussionFilterType, graphql_name='filter', default=None)),
        ('sort_order', sgqlc.types.Arg(DiscussionSortOrderType, graphql_name='sortOrder', default=None)),
        ('root_entries', sgqlc.types.Arg(Boolean, graphql_name='rootEntries', default=None)),
        ('unread_before', sgqlc.types.Arg(String, graphql_name='unreadBefore', default=None)),
))
    )
    entry_counts = sgqlc.types.Field(DiscussionEntryCounts, graphql_name='entryCounts')
    group_set = sgqlc.types.Field('GroupSet', graphql_name='groupSet')
    initial_post_required_for_current_user = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='initialPostRequiredForCurrentUser')
    is_announcement = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isAnnouncement')
    is_anonymous_author = sgqlc.types.Field(Boolean, graphql_name='isAnonymousAuthor')
    is_section_specific = sgqlc.types.Field(Boolean, graphql_name='isSectionSpecific')
    last_reply_at = sgqlc.types.Field(DateTime, graphql_name='lastReplyAt')
    lock_at = sgqlc.types.Field(DateTime, graphql_name='lockAt')
    locked = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='locked')
    mentionable_users_connection = sgqlc.types.Field(MessageableUserConnection, graphql_name='mentionableUsersConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
        ('search_term', sgqlc.types.Arg(String, graphql_name='searchTerm', default=None)),
))
    )
    message = sgqlc.types.Field(String, graphql_name='message')
    only_graders_can_rate = sgqlc.types.Field(Boolean, graphql_name='onlyGradersCanRate')
    permissions = sgqlc.types.Field(DiscussionPermissions, graphql_name='permissions')
    podcast_enabled = sgqlc.types.Field(Boolean, graphql_name='podcastEnabled')
    podcast_has_student_posts = sgqlc.types.Field(Boolean, graphql_name='podcastHasStudentPosts')
    position = sgqlc.types.Field(Int, graphql_name='position')
    posted_at = sgqlc.types.Field(DateTime, graphql_name='postedAt')
    published = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='published')
    require_initial_post = sgqlc.types.Field(Boolean, graphql_name='requireInitialPost')
    root_entries_total_pages = sgqlc.types.Field(Int, graphql_name='rootEntriesTotalPages', args=sgqlc.types.ArgDict((
        ('per_page', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='perPage', default=None)),
        ('search_term', sgqlc.types.Arg(String, graphql_name='searchTerm', default=None)),
        ('filter', sgqlc.types.Arg(DiscussionFilterType, graphql_name='filter', default=None)),
        ('sort_order', sgqlc.types.Arg(DiscussionSortOrderType, graphql_name='sortOrder', default=None)),
))
    )
    root_topic = sgqlc.types.Field('Discussion', graphql_name='rootTopic')
    search_entry_count = sgqlc.types.Field(Int, graphql_name='searchEntryCount', args=sgqlc.types.ArgDict((
        ('search_term', sgqlc.types.Arg(String, graphql_name='searchTerm', default=None)),
        ('filter', sgqlc.types.Arg(DiscussionFilterType, graphql_name='filter', default=None)),
))
    )
    sort_by_rating = sgqlc.types.Field(Boolean, graphql_name='sortByRating')
    subscribed = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='subscribed')
    title = sgqlc.types.Field(String, graphql_name='title')
    todo_date = sgqlc.types.Field(ISO8601DateTime, graphql_name='todoDate')
    user_count = sgqlc.types.Field(Int, graphql_name='userCount')


class DiscussionEntry(sgqlc.types.Type, Node, Timestamped, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('all_root_entries', 'anonymous_author', 'attachment', 'author', 'deleted', 'depth', 'discussion_entry_versions_connection', 'discussion_subentries_connection', 'discussion_topic', 'discussion_topic_id', 'editor', 'entry_participant', 'isolated_entry_id', 'last_reply', 'message', 'parent_id', 'permissions', 'preview_message', 'quoted_entry', 'rating_count', 'rating_sum', 'report_type_counts', 'root_entry', 'root_entry_id', 'root_entry_participant_counts', 'subentries_count')
    all_root_entries = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('DiscussionEntry')), graphql_name='allRootEntries')
    anonymous_author = sgqlc.types.Field(AnonymousUser, graphql_name='anonymousAuthor')
    attachment = sgqlc.types.Field('File', graphql_name='attachment')
    author = sgqlc.types.Field('User', graphql_name='author', args=sgqlc.types.ArgDict((
        ('course_id', sgqlc.types.Arg(String, graphql_name='courseId', default=None)),
        ('role_types', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='roleTypes', default=None)),
        ('built_in_only', sgqlc.types.Arg(Boolean, graphql_name='builtInOnly', default=None)),
))
    )
    deleted = sgqlc.types.Field(Boolean, graphql_name='deleted')
    depth = sgqlc.types.Field(Int, graphql_name='depth')
    discussion_entry_versions_connection = sgqlc.types.Field(DiscussionEntryVersionConnection, graphql_name='discussionEntryVersionsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    discussion_subentries_connection = sgqlc.types.Field(DiscussionEntryConnection, graphql_name='discussionSubentriesConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
        ('sort_order', sgqlc.types.Arg(DiscussionSortOrderType, graphql_name='sortOrder', default=None)),
        ('relative_entry_id', sgqlc.types.Arg(ID, graphql_name='relativeEntryId', default=None)),
        ('before_relative_entry', sgqlc.types.Arg(Boolean, graphql_name='beforeRelativeEntry', default=None)),
        ('include_relative_entry', sgqlc.types.Arg(Boolean, graphql_name='includeRelativeEntry', default=None)),
))
    )
    discussion_topic = sgqlc.types.Field(sgqlc.types.non_null(Discussion), graphql_name='discussionTopic')
    discussion_topic_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='discussionTopicId')
    editor = sgqlc.types.Field('User', graphql_name='editor', args=sgqlc.types.ArgDict((
        ('course_id', sgqlc.types.Arg(String, graphql_name='courseId', default=None)),
        ('role_types', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='roleTypes', default=None)),
        ('built_in_only', sgqlc.types.Arg(Boolean, graphql_name='builtInOnly', default=None)),
))
    )
    entry_participant = sgqlc.types.Field(EntryParticipant, graphql_name='entryParticipant')
    isolated_entry_id = sgqlc.types.Field(ID, graphql_name='isolatedEntryId')
    last_reply = sgqlc.types.Field('DiscussionEntry', graphql_name='lastReply')
    message = sgqlc.types.Field(String, graphql_name='message')
    parent_id = sgqlc.types.Field(ID, graphql_name='parentId')
    permissions = sgqlc.types.Field(DiscussionEntryPermissions, graphql_name='permissions')
    preview_message = sgqlc.types.Field(String, graphql_name='previewMessage')
    quoted_entry = sgqlc.types.Field('DiscussionEntry', graphql_name='quotedEntry')
    rating_count = sgqlc.types.Field(Int, graphql_name='ratingCount')
    rating_sum = sgqlc.types.Field(Int, graphql_name='ratingSum')
    report_type_counts = sgqlc.types.Field(DiscussionEntryReportTypeCounts, graphql_name='reportTypeCounts')
    root_entry = sgqlc.types.Field('DiscussionEntry', graphql_name='rootEntry')
    root_entry_id = sgqlc.types.Field(ID, graphql_name='rootEntryId')
    root_entry_participant_counts = sgqlc.types.Field(DiscussionEntryCounts, graphql_name='rootEntryParticipantCounts')
    subentries_count = sgqlc.types.Field(Int, graphql_name='subentriesCount')


class DiscussionEntryDraft(sgqlc.types.Type, Timestamped, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('attachment', 'discussion_entry_id', 'discussion_topic_id', 'id', 'message', 'parent_id', 'root_entry_id')
    attachment = sgqlc.types.Field('File', graphql_name='attachment')
    discussion_entry_id = sgqlc.types.Field(ID, graphql_name='discussionEntryId')
    discussion_topic_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='discussionTopicId')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='message')
    parent_id = sgqlc.types.Field(ID, graphql_name='parentId')
    root_entry_id = sgqlc.types.Field(ID, graphql_name='rootEntryId')


class DiscussionEntryVersion(sgqlc.types.Type, Timestamped, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('id', 'message', 'version')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='message')
    version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='version')


class Enrollment(sgqlc.types.Type, Node, Timestamped, LegacyIDInterface, AssetString):
    __schema__ = canvas_schema
    __field_names__ = ('associated_user', 'can_be_removed', 'concluded', 'course', 'course_section_id', 'grades', 'html_url', 'last_activity_at', 'section', 'sis_import_id', 'sis_role', 'state', 'total_activity_time', 'type', 'user')
    associated_user = sgqlc.types.Field('User', graphql_name='associatedUser')
    can_be_removed = sgqlc.types.Field(Boolean, graphql_name='canBeRemoved')
    concluded = sgqlc.types.Field(Boolean, graphql_name='concluded')
    course = sgqlc.types.Field(Course, graphql_name='course')
    course_section_id = sgqlc.types.Field(ID, graphql_name='courseSectionId')
    grades = sgqlc.types.Field(Grades, graphql_name='grades', args=sgqlc.types.ArgDict((
        ('grading_period_id', sgqlc.types.Arg(ID, graphql_name='gradingPeriodId', default=None)),
))
    )
    html_url = sgqlc.types.Field(URL, graphql_name='htmlUrl')
    last_activity_at = sgqlc.types.Field(DateTime, graphql_name='lastActivityAt')
    section = sgqlc.types.Field('Section', graphql_name='section')
    sis_import_id = sgqlc.types.Field(ID, graphql_name='sisImportId')
    sis_role = sgqlc.types.Field(String, graphql_name='sisRole')
    state = sgqlc.types.Field(sgqlc.types.non_null(EnrollmentWorkflowState), graphql_name='state')
    total_activity_time = sgqlc.types.Field(Int, graphql_name='totalActivityTime')
    type = sgqlc.types.Field(sgqlc.types.non_null(EnrollmentType), graphql_name='type')
    user = sgqlc.types.Field('User', graphql_name='user')


class ExternalTool(sgqlc.types.Type, Timestamped, ModuleItemInterface, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('description', 'name', 'settings', 'state', 'url')
    description = sgqlc.types.Field(String, graphql_name='description')
    name = sgqlc.types.Field(String, graphql_name='name')
    settings = sgqlc.types.Field(ExternalToolSettings, graphql_name='settings')
    state = sgqlc.types.Field(ExternalToolState, graphql_name='state')
    url = sgqlc.types.Field(URL, graphql_name='url')


class ExternalUrl(sgqlc.types.Type, Timestamped, ModuleItemInterface, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('title', 'url')
    title = sgqlc.types.Field(String, graphql_name='title')
    url = sgqlc.types.Field(String, graphql_name='url')


class File(sgqlc.types.Type, Node, ModuleItemInterface, Timestamped, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('content_type', 'display_name', 'mime_class', 'size', 'submission_preview_url', 'thumbnail_url', 'url', 'usage_rights')
    content_type = sgqlc.types.Field(String, graphql_name='contentType')
    display_name = sgqlc.types.Field(String, graphql_name='displayName')
    mime_class = sgqlc.types.Field(String, graphql_name='mimeClass')
    size = sgqlc.types.Field(String, graphql_name='size')
    submission_preview_url = sgqlc.types.Field(URL, graphql_name='submissionPreviewUrl', args=sgqlc.types.ArgDict((
        ('submission_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='submissionId', default=None)),
))
    )
    thumbnail_url = sgqlc.types.Field(URL, graphql_name='thumbnailUrl')
    url = sgqlc.types.Field(URL, graphql_name='url')
    usage_rights = sgqlc.types.Field('UsageRights', graphql_name='usageRights')


class GradingPeriod(sgqlc.types.Type, Node, Timestamped, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('close_date', 'display_totals', 'end_date', 'is_last', 'start_date', 'title', 'weight')
    close_date = sgqlc.types.Field(DateTime, graphql_name='closeDate')
    display_totals = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='displayTotals')
    end_date = sgqlc.types.Field(DateTime, graphql_name='endDate')
    is_last = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isLast')
    start_date = sgqlc.types.Field(DateTime, graphql_name='startDate')
    title = sgqlc.types.Field(String, graphql_name='title')
    weight = sgqlc.types.Field(Float, graphql_name='weight')


class GradingPeriodGroup(sgqlc.types.Type, Node, Timestamped, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('display_totals', 'enrollment_term_ids', 'grading_periods_connection', 'title', 'weighted')
    display_totals = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='displayTotals')
    enrollment_term_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='enrollmentTermIds')
    grading_periods_connection = sgqlc.types.Field(GradingPeriodConnection, graphql_name='gradingPeriodsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    title = sgqlc.types.Field(String, graphql_name='title')
    weighted = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='weighted')


class Group(sgqlc.types.Type, Node, Timestamped, LegacyIDInterface, AssetString):
    __schema__ = canvas_schema
    __field_names__ = ('can_message', 'member', 'members_connection', 'members_count', 'name', 'sis_id')
    can_message = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='canMessage')
    member = sgqlc.types.Field('GroupMembership', graphql_name='member', args=sgqlc.types.ArgDict((
        ('user_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='userId', default=None)),
))
    )
    members_connection = sgqlc.types.Field(GroupMembershipConnection, graphql_name='membersConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    members_count = sgqlc.types.Field(Int, graphql_name='membersCount')
    name = sgqlc.types.Field(String, graphql_name='name')
    sis_id = sgqlc.types.Field(String, graphql_name='sisId')


class GroupMembership(sgqlc.types.Type, Timestamped, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('state', 'user')
    state = sgqlc.types.Field(sgqlc.types.non_null(GroupMembershipState), graphql_name='state')
    user = sgqlc.types.Field('User', graphql_name='user')


class GroupSet(sgqlc.types.Type, Node, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('auto_leader', 'current_group', 'groups_connection', 'member_limit', 'name', 'self_signup', 'sis_id')
    auto_leader = sgqlc.types.Field(AutoLeaderPolicy, graphql_name='autoLeader')
    current_group = sgqlc.types.Field(Group, graphql_name='currentGroup')
    groups_connection = sgqlc.types.Field(GroupConnection, graphql_name='groupsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    member_limit = sgqlc.types.Field(Int, graphql_name='memberLimit')
    name = sgqlc.types.Field(String, graphql_name='name')
    self_signup = sgqlc.types.Field(sgqlc.types.non_null(SelfSignupPolicy), graphql_name='selfSignup')
    sis_id = sgqlc.types.Field(String, graphql_name='sisId')


class InternalSetting(sgqlc.types.Type, Node, Timestamped, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('name', 'secret', 'value')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    secret = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='secret')
    value = sgqlc.types.Field(String, graphql_name='value')


class LearningOutcome(sgqlc.types.Type, Node, LegacyIDInterface, Timestamped):
    __schema__ = canvas_schema
    __field_names__ = ('alignments', 'assessed', 'calculation_int', 'calculation_method', 'can_edit', 'context_id', 'context_type', 'description', 'display_name', 'friendly_description', 'is_imported', 'mastery_points', 'points_possible', 'ratings', 'title', 'vendor_guid')
    alignments = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('OutcomeAlignment')), graphql_name='alignments', args=sgqlc.types.ArgDict((
        ('context_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='contextId', default=None)),
        ('context_type', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='contextType', default=None)),
))
    )
    assessed = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='assessed')
    calculation_int = sgqlc.types.Field(Int, graphql_name='calculationInt')
    calculation_method = sgqlc.types.Field(String, graphql_name='calculationMethod')
    can_edit = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='canEdit')
    context_id = sgqlc.types.Field(ID, graphql_name='contextId')
    context_type = sgqlc.types.Field(String, graphql_name='contextType')
    description = sgqlc.types.Field(String, graphql_name='description')
    display_name = sgqlc.types.Field(String, graphql_name='displayName')
    friendly_description = sgqlc.types.Field('OutcomeFriendlyDescriptionType', graphql_name='friendlyDescription', args=sgqlc.types.ArgDict((
        ('context_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='contextId', default=None)),
        ('context_type', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='contextType', default=None)),
))
    )
    is_imported = sgqlc.types.Field(Boolean, graphql_name='isImported', args=sgqlc.types.ArgDict((
        ('target_context_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='targetContextId', default=None)),
        ('target_context_type', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='targetContextType', default=None)),
))
    )
    mastery_points = sgqlc.types.Field(Float, graphql_name='masteryPoints')
    points_possible = sgqlc.types.Field(Float, graphql_name='pointsPossible')
    ratings = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ProficiencyRating')), graphql_name='ratings')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    vendor_guid = sgqlc.types.Field(String, graphql_name='vendorGuid')


class LearningOutcomeGroup(sgqlc.types.Type, Node, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('can_edit', 'child_groups', 'child_groups_count', 'context_id', 'context_type', 'description', 'not_imported_outcomes_count', 'outcomes', 'outcomes_count', 'parent_outcome_group', 'title', 'vendor_guid')
    can_edit = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='canEdit')
    child_groups = sgqlc.types.Field(LearningOutcomeGroupConnection, graphql_name='childGroups', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    child_groups_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='childGroupsCount')
    context_id = sgqlc.types.Field(ID, graphql_name='contextId')
    context_type = sgqlc.types.Field(String, graphql_name='contextType')
    description = sgqlc.types.Field(String, graphql_name='description')
    not_imported_outcomes_count = sgqlc.types.Field(Int, graphql_name='notImportedOutcomesCount', args=sgqlc.types.ArgDict((
        ('target_group_id', sgqlc.types.Arg(ID, graphql_name='targetGroupId', default=None)),
))
    )
    outcomes = sgqlc.types.Field(sgqlc.types.non_null(ContentTagConnection), graphql_name='outcomes', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
        ('search_query', sgqlc.types.Arg(String, graphql_name='searchQuery', default=None)),
        ('filter', sgqlc.types.Arg(String, graphql_name='filter', default=None)),
))
    )
    outcomes_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='outcomesCount', args=sgqlc.types.ArgDict((
        ('search_query', sgqlc.types.Arg(String, graphql_name='searchQuery', default=None)),
))
    )
    parent_outcome_group = sgqlc.types.Field('LearningOutcomeGroup', graphql_name='parentOutcomeGroup')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    vendor_guid = sgqlc.types.Field(String, graphql_name='vendorGuid')


class MediaObject(sgqlc.types.Type, Node):
    __schema__ = canvas_schema
    __field_names__ = ('_id', 'can_add_captions', 'media_download_url', 'media_sources', 'media_tracks', 'media_type', 'title')
    _id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='_id')
    can_add_captions = sgqlc.types.Field(Boolean, graphql_name='canAddCaptions')
    media_download_url = sgqlc.types.Field(String, graphql_name='mediaDownloadUrl')
    media_sources = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(MediaSource)), graphql_name='mediaSources')
    media_tracks = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('MediaTrack')), graphql_name='mediaTracks')
    media_type = sgqlc.types.Field(MediaType, graphql_name='mediaType')
    title = sgqlc.types.Field(String, graphql_name='title')


class MediaTrack(sgqlc.types.Type, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('content', 'kind', 'locale', 'media_object', 'webvtt_content')
    content = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='content')
    kind = sgqlc.types.Field(String, graphql_name='kind')
    locale = sgqlc.types.Field(String, graphql_name='locale')
    media_object = sgqlc.types.Field(MediaObject, graphql_name='mediaObject')
    webvtt_content = sgqlc.types.Field(String, graphql_name='webvttContent')


class MessageableContext(sgqlc.types.Type, Node):
    __schema__ = canvas_schema
    __field_names__ = ('avatar_url', 'item_count', 'name', 'permissions', 'user_count')
    avatar_url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='avatarUrl')
    item_count = sgqlc.types.Field(Int, graphql_name='itemCount')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    permissions = sgqlc.types.Field(MessagePermissions, graphql_name='permissions')
    user_count = sgqlc.types.Field(Int, graphql_name='userCount')


class MessageableUser(sgqlc.types.Type, Node):
    __schema__ = canvas_schema
    __field_names__ = ('_id', 'common_courses_connection', 'common_groups_connection', 'name', 'observer_enrollments_connection', 'short_name')
    _id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='_id')
    common_courses_connection = sgqlc.types.Field(EnrollmentConnection, graphql_name='commonCoursesConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    common_groups_connection = sgqlc.types.Field(GroupConnection, graphql_name='commonGroupsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    observer_enrollments_connection = sgqlc.types.Field(EnrollmentConnection, graphql_name='observerEnrollmentsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
        ('context_code', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='contextCode', default=None)),
))
    )
    short_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='shortName')


class Module(sgqlc.types.Type, Node, Timestamped, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('module_items', 'name', 'position', 'unlock_at')
    module_items = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('ModuleItem')), graphql_name='moduleItems')
    name = sgqlc.types.Field(String, graphql_name='name')
    position = sgqlc.types.Field(Int, graphql_name='position')
    unlock_at = sgqlc.types.Field(DateTime, graphql_name='unlockAt')


class ModuleExternalTool(sgqlc.types.Type, Timestamped, ModuleItemInterface, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('url',)
    url = sgqlc.types.Field(String, graphql_name='url')


class ModuleItem(sgqlc.types.Type, Node, Timestamped, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('content', 'module', 'next', 'previous', 'url')
    content = sgqlc.types.Field(ModuleItemInterface, graphql_name='content')
    module = sgqlc.types.Field(Module, graphql_name='module')
    next = sgqlc.types.Field('ModuleItem', graphql_name='next')
    previous = sgqlc.types.Field('ModuleItem', graphql_name='previous')
    url = sgqlc.types.Field(URL, graphql_name='url')


class Notification(sgqlc.types.Type, Node, Timestamped, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('category', 'category_description', 'category_display_name', 'name', 'workflow_state')
    category = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='category')
    category_description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='categoryDescription')
    category_display_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='categoryDisplayName')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    workflow_state = sgqlc.types.Field(String, graphql_name='workflowState')


class NotificationPolicy(sgqlc.types.Type, Node, Timestamped, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('communication_channel_id', 'frequency', 'notification')
    communication_channel_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='communicationChannelId')
    frequency = sgqlc.types.Field(String, graphql_name='frequency')
    notification = sgqlc.types.Field(Notification, graphql_name='notification')


class OutcomeAlignment(sgqlc.types.Type, Timestamped):
    __schema__ = canvas_schema
    __field_names__ = ('_id', 'alignments_count', 'assignment_content_type', 'assignment_workflow_state', 'content_id', 'content_type', 'context_id', 'context_type', 'learning_outcome_id', 'module_id', 'module_name', 'module_url', 'module_workflow_state', 'quiz_items', 'title', 'url')
    _id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='_id')
    alignments_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='alignmentsCount')
    assignment_content_type = sgqlc.types.Field(String, graphql_name='assignmentContentType')
    assignment_workflow_state = sgqlc.types.Field(String, graphql_name='assignmentWorkflowState')
    content_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contentId')
    content_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='contentType')
    context_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contextId')
    context_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='contextType')
    learning_outcome_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='learningOutcomeId')
    module_id = sgqlc.types.Field(String, graphql_name='moduleId')
    module_name = sgqlc.types.Field(String, graphql_name='moduleName')
    module_url = sgqlc.types.Field(String, graphql_name='moduleUrl')
    module_workflow_state = sgqlc.types.Field(String, graphql_name='moduleWorkflowState')
    quiz_items = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(QuizItem)), graphql_name='quizItems')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='url')


class OutcomeCalculationMethod(sgqlc.types.Type, Node, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('calculation_int', 'calculation_method', 'context_id', 'context_type', 'locked')
    calculation_int = sgqlc.types.Field(Int, graphql_name='calculationInt')
    calculation_method = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='calculationMethod')
    context_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contextId')
    context_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='contextType')
    locked = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='locked')


class OutcomeFriendlyDescriptionType(sgqlc.types.Type, Node, Timestamped, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('context_id', 'context_type', 'description', 'learning_outcome_id', 'workflow_state')
    context_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contextId')
    context_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='contextType')
    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')
    learning_outcome_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='learningOutcomeId')
    workflow_state = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='workflowState')


class OutcomeProficiency(sgqlc.types.Type, Node, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('context_id', 'context_type', 'locked', 'proficiency_ratings_connection')
    context_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contextId')
    context_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='contextType')
    locked = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='locked')
    proficiency_ratings_connection = sgqlc.types.Field(ProficiencyRatingConnection, graphql_name='proficiencyRatingsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )


class Page(sgqlc.types.Type, Node, Timestamped, ModuleItemInterface, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('title',)
    title = sgqlc.types.Field(String, graphql_name='title')


class PostPolicy(sgqlc.types.Type, Node, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('assignment', 'course', 'post_manually')
    assignment = sgqlc.types.Field(Assignment, graphql_name='assignment')
    course = sgqlc.types.Field(sgqlc.types.non_null(Course), graphql_name='course')
    post_manually = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='postManually')


class ProficiencyRating(sgqlc.types.Type, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('color', 'description', 'mastery', 'points')
    color = sgqlc.types.Field(String, graphql_name='color')
    description = sgqlc.types.Field(String, graphql_name='description')
    mastery = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='mastery')
    points = sgqlc.types.Field(Float, graphql_name='points')


class Progress(sgqlc.types.Type, Node, Timestamped, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('completion', 'context', 'message', 'state', 'tag')
    completion = sgqlc.types.Field(Int, graphql_name='completion')
    context = sgqlc.types.Field('ProgressContext', graphql_name='context')
    message = sgqlc.types.Field(String, graphql_name='message')
    state = sgqlc.types.Field(sgqlc.types.non_null(ProgressState), graphql_name='state')
    tag = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='tag')


class Quiz(sgqlc.types.Type, Node, Timestamped, ModuleItemInterface, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ()


class Rubric(sgqlc.types.Type, Node, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('criteria', 'criteria_count', 'free_form_criterion_comments', 'hide_score_total', 'points_possible', 'title', 'workflow_state')
    criteria = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('RubricCriterion'))), graphql_name='criteria')
    criteria_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='criteriaCount')
    free_form_criterion_comments = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='freeFormCriterionComments')
    hide_score_total = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hideScoreTotal')
    points_possible = sgqlc.types.Field(Float, graphql_name='pointsPossible')
    title = sgqlc.types.Field(String, graphql_name='title')
    workflow_state = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='workflowState')


class RubricAssessment(sgqlc.types.Type, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('artifact_attempt', 'assessment_ratings', 'assessment_type', 'assessor', 'rubric_association', 'score', 'user')
    artifact_attempt = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='artifactAttempt')
    assessment_ratings = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(RubricAssessmentRating))), graphql_name='assessmentRatings')
    assessment_type = sgqlc.types.Field(sgqlc.types.non_null(AssessmentType), graphql_name='assessmentType')
    assessor = sgqlc.types.Field('User', graphql_name='assessor')
    rubric_association = sgqlc.types.Field('RubricAssociation', graphql_name='rubricAssociation')
    score = sgqlc.types.Field(Float, graphql_name='score')
    user = sgqlc.types.Field('User', graphql_name='user')


class RubricAssociation(sgqlc.types.Type, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('hide_outcome_results', 'hide_points', 'hide_score_total', 'use_for_grading')
    hide_outcome_results = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hideOutcomeResults')
    hide_points = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hidePoints')
    hide_score_total = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hideScoreTotal')
    use_for_grading = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='useForGrading')


class RubricCriterion(sgqlc.types.Type, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('criterion_use_range', 'description', 'ignore_for_scoring', 'long_description', 'mastery_points', 'outcome', 'points', 'ratings')
    criterion_use_range = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='criterionUseRange')
    description = sgqlc.types.Field(String, graphql_name='description')
    ignore_for_scoring = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='ignoreForScoring')
    long_description = sgqlc.types.Field(String, graphql_name='longDescription')
    mastery_points = sgqlc.types.Field(Float, graphql_name='masteryPoints')
    outcome = sgqlc.types.Field(LearningOutcome, graphql_name='outcome')
    points = sgqlc.types.Field(Float, graphql_name='points')
    ratings = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('RubricRating')), graphql_name='ratings')


class RubricRating(sgqlc.types.Type, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('description', 'long_description', 'points', 'rubric_id')
    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')
    long_description = sgqlc.types.Field(String, graphql_name='longDescription')
    points = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='points')
    rubric_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='rubricId')


class Section(sgqlc.types.Type, Node, Timestamped, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('name', 'sis_id', 'user_count')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    sis_id = sgqlc.types.Field(String, graphql_name='sisId')
    user_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='userCount')


class StandardGradeStatus(sgqlc.types.Type, LegacyIDInterface, Node):
    __schema__ = canvas_schema
    __field_names__ = ('color', 'name')
    color = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='color')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')


class SubHeader(sgqlc.types.Type, ModuleItemInterface):
    __schema__ = canvas_schema
    __field_names__ = ('title',)
    title = sgqlc.types.Field(String, graphql_name='title')


class Submission(sgqlc.types.Type, Node, Timestamped, SubmissionInterface, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('cached_due_date', 'grading_period_id', 'read_state', 'redo_request', 'student_entered_score', 'submission_histories_connection', 'user_id')
    cached_due_date = sgqlc.types.Field(DateTime, graphql_name='cachedDueDate')
    grading_period_id = sgqlc.types.Field(ID, graphql_name='gradingPeriodId')
    read_state = sgqlc.types.Field(String, graphql_name='readState')
    redo_request = sgqlc.types.Field(Boolean, graphql_name='redoRequest')
    student_entered_score = sgqlc.types.Field(Float, graphql_name='studentEnteredScore')
    submission_histories_connection = sgqlc.types.Field(SubmissionHistoryConnection, graphql_name='submissionHistoriesConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
        ('filter', sgqlc.types.Arg(SubmissionHistoryFilterInput, graphql_name='filter', default={})),
))
    )
    user_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='userId')


class SubmissionComment(sgqlc.types.Type, Timestamped, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('assignment', 'attachments', 'attempt', 'author', 'comment', 'course', 'id', 'media_object', 'read', 'submission_id')
    assignment = sgqlc.types.Field(Assignment, graphql_name='assignment')
    attachments = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(File)), graphql_name='attachments')
    attempt = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='attempt')
    author = sgqlc.types.Field('User', graphql_name='author')
    comment = sgqlc.types.Field(String, graphql_name='comment')
    course = sgqlc.types.Field(Course, graphql_name='course')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    media_object = sgqlc.types.Field(MediaObject, graphql_name='mediaObject')
    read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='read')
    submission_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='submissionId')


class SubmissionDraft(sgqlc.types.Type, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('active_submission_type', 'attachments', 'body', 'external_tool', 'lti_launch_url', 'media_object', 'meets_assignment_criteria', 'meets_basic_lti_launch_criteria', 'meets_media_recording_criteria', 'meets_student_annotation_criteria', 'meets_text_entry_criteria', 'meets_upload_criteria', 'meets_url_criteria', 'resource_link_lookup_uuid', 'submission_attempt', 'url')
    active_submission_type = sgqlc.types.Field(DraftableSubmissionType, graphql_name='activeSubmissionType')
    attachments = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(File)), graphql_name='attachments')
    body = sgqlc.types.Field(String, graphql_name='body', args=sgqlc.types.ArgDict((
        ('rewrite_urls', sgqlc.types.Arg(Boolean, graphql_name='rewriteUrls', default=None)),
))
    )
    external_tool = sgqlc.types.Field(ExternalTool, graphql_name='externalTool')
    lti_launch_url = sgqlc.types.Field(URL, graphql_name='ltiLaunchUrl')
    media_object = sgqlc.types.Field(MediaObject, graphql_name='mediaObject')
    meets_assignment_criteria = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='meetsAssignmentCriteria')
    meets_basic_lti_launch_criteria = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='meetsBasicLtiLaunchCriteria')
    meets_media_recording_criteria = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='meetsMediaRecordingCriteria')
    meets_student_annotation_criteria = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='meetsStudentAnnotationCriteria')
    meets_text_entry_criteria = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='meetsTextEntryCriteria')
    meets_upload_criteria = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='meetsUploadCriteria')
    meets_url_criteria = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='meetsUrlCriteria')
    resource_link_lookup_uuid = sgqlc.types.Field(String, graphql_name='resourceLinkLookupUuid')
    submission_attempt = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='submissionAttempt')
    url = sgqlc.types.Field(URL, graphql_name='url')


class SubmissionHistory(sgqlc.types.Type, Timestamped, SubmissionInterface):
    __schema__ = canvas_schema
    __field_names__ = ('root_id',)
    root_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='rootId')


class Term(sgqlc.types.Type, Node, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('courses_connection', 'end_at', 'name', 'sis_id', 'sis_term_id', 'start_at')
    courses_connection = sgqlc.types.Field(CourseConnection, graphql_name='coursesConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    end_at = sgqlc.types.Field(DateTime, graphql_name='endAt')
    name = sgqlc.types.Field(String, graphql_name='name')
    sis_id = sgqlc.types.Field(String, graphql_name='sisId')
    sis_term_id = sgqlc.types.Field(ID, graphql_name='sisTermId')
    start_at = sgqlc.types.Field(DateTime, graphql_name='startAt')


class UsageRights(sgqlc.types.Type, Node, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('legal_copyright', 'license', 'use_justification')
    legal_copyright = sgqlc.types.Field(String, graphql_name='legalCopyright')
    license = sgqlc.types.Field(String, graphql_name='license')
    use_justification = sgqlc.types.Field(String, graphql_name='useJustification')


class User(sgqlc.types.Type, Node, Timestamped, LegacyIDInterface):
    __schema__ = canvas_schema
    __field_names__ = ('avatar_url', 'comment_bank_items_connection', 'conversations_connection', 'course_roles', 'discussions_splitscreen_view', 'email', 'enrollments', 'favorite_courses_connection', 'favorite_groups_connection', 'groups', 'html_url', 'inbox_labels', 'integration_id', 'login_id', 'name', 'notification_preferences', 'notification_preferences_enabled', 'pronouns', 'recipients', 'recipients_observers', 'short_name', 'sis_id', 'sortable_name', 'summary_analytics', 'total_recipients', 'uuid', 'viewable_submissions_connection')
    avatar_url = sgqlc.types.Field(URL, graphql_name='avatarUrl')
    comment_bank_items_connection = sgqlc.types.Field(CommentBankItemConnection, graphql_name='commentBankItemsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
        ('query', sgqlc.types.Arg(String, graphql_name='query', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
))
    )
    conversations_connection = sgqlc.types.Field(ConversationParticipantConnection, graphql_name='conversationsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
        ('scope', sgqlc.types.Arg(String, graphql_name='scope', default=None)),
        ('filter', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='filter', default=None)),
))
    )
    course_roles = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='courseRoles', args=sgqlc.types.ArgDict((
        ('course_id', sgqlc.types.Arg(String, graphql_name='courseId', default=None)),
        ('role_types', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='roleTypes', default=None)),
        ('built_in_only', sgqlc.types.Arg(Boolean, graphql_name='builtInOnly', default=None)),
))
    )
    discussions_splitscreen_view = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='discussionsSplitscreenView')
    email = sgqlc.types.Field(String, graphql_name='email')
    enrollments = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Enrollment))), graphql_name='enrollments', args=sgqlc.types.ArgDict((
        ('course_id', sgqlc.types.Arg(ID, graphql_name='courseId', default=None)),
        ('current_only', sgqlc.types.Arg(Boolean, graphql_name='currentOnly', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='orderBy', default=None)),
        ('exclude_concluded', sgqlc.types.Arg(Boolean, graphql_name='excludeConcluded', default=None)),
))
    )
    favorite_courses_connection = sgqlc.types.Field(CourseConnection, graphql_name='favoriteCoursesConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    favorite_groups_connection = sgqlc.types.Field(GroupConnection, graphql_name='favoriteGroupsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    groups = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Group)), graphql_name='groups')
    html_url = sgqlc.types.Field(URL, graphql_name='htmlUrl', args=sgqlc.types.ArgDict((
        ('course_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='courseId', default=None)),
))
    )
    inbox_labels = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='inboxLabels')
    integration_id = sgqlc.types.Field(String, graphql_name='integrationId')
    login_id = sgqlc.types.Field(String, graphql_name='loginId')
    name = sgqlc.types.Field(String, graphql_name='name')
    notification_preferences = sgqlc.types.Field(NotificationPreferences, graphql_name='notificationPreferences')
    notification_preferences_enabled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='notificationPreferencesEnabled', args=sgqlc.types.ArgDict((
        ('account_id', sgqlc.types.Arg(ID, graphql_name='accountId', default=None)),
        ('course_id', sgqlc.types.Arg(ID, graphql_name='courseId', default=None)),
        ('context_type', sgqlc.types.Arg(sgqlc.types.non_null(NotificationPreferencesContextType), graphql_name='contextType', default=None)),
))
    )
    pronouns = sgqlc.types.Field(String, graphql_name='pronouns')
    recipients = sgqlc.types.Field(Recipients, graphql_name='recipients', args=sgqlc.types.ArgDict((
        ('search', sgqlc.types.Arg(String, graphql_name='search', default=None)),
        ('context', sgqlc.types.Arg(String, graphql_name='context', default=None)),
))
    )
    recipients_observers = sgqlc.types.Field(MessageableUserConnection, graphql_name='recipientsObservers', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
        ('recipient_ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='recipientIds', default=None)),
        ('context_code', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='contextCode', default=None)),
))
    )
    short_name = sgqlc.types.Field(String, graphql_name='shortName')
    sis_id = sgqlc.types.Field(String, graphql_name='sisId')
    sortable_name = sgqlc.types.Field(String, graphql_name='sortableName')
    summary_analytics = sgqlc.types.Field(StudentSummaryAnalytics, graphql_name='summaryAnalytics', args=sgqlc.types.ArgDict((
        ('course_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='courseId', default=None)),
))
    )
    total_recipients = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalRecipients', args=sgqlc.types.ArgDict((
        ('context', sgqlc.types.Arg(String, graphql_name='context', default=None)),
))
    )
    uuid = sgqlc.types.Field(String, graphql_name='uuid')
    viewable_submissions_connection = sgqlc.types.Field(SubmissionConnection, graphql_name='viewableSubmissionsConnection', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
        ('filter', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='filter', default=None)),
))
    )



########################################################################
# Unions
########################################################################
class AssignmentOverrideSet(sgqlc.types.Union):
    __schema__ = canvas_schema
    __types__ = (AdhocStudents, Course, Group, Noop, Section)


class ContentTagContent(sgqlc.types.Union):
    __schema__ = canvas_schema
    __types__ = (LearningOutcome,)


class Lockable(sgqlc.types.Union):
    __schema__ = canvas_schema
    __types__ = (Assignment, Discussion, Module, Page, Quiz)


class ProgressContext(sgqlc.types.Union):
    __schema__ = canvas_schema
    __types__ = (Assignment, Course, File, GroupSet, User)


class TurnitinContext(sgqlc.types.Union):
    __schema__ = canvas_schema
    __types__ = (File, Submission)



########################################################################
# Schema Entry Points
########################################################################
canvas_schema.query_type = Query
canvas_schema.mutation_type = Mutation
canvas_schema.subscription_type = None

