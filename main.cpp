#include <stdio.h>
#include <string.h>
#include <emscripten.h>
#include <emscripten/html5.h>
#include <GLES2/gl2.h>
#include <GLES2/gl2ext.h>

#define CHECK(VALUE, LABEL) \
    (VALUE == EMSCRIPTEN_RESULT_SUCCESS) \
    ? printf("[INFO]: %s: %s\n", LABEL, "Success") \
    : printf("[WARN]: %s: %s\n", LABEL, "Error")

const char* vertex_source = \
"attribute vec4 vertex;" \
"varying vec2 position;" \
"uniform vec4 cursor;" \
"varying vec2 v_cursor;" \
"void main()" \
"{" \
"    v_cursor = cursor.xy / cursor.zw;" \
"    position = vertex.xy;" \
"    gl_Position = vertex;" \
"    gl_PointSize = 3.0;" \
"}";

const char* fragment_source = \
"precision highp float;" \
"varying vec2 position;" \
"varying vec2 v_cursor;" \
"void main()" \
"{" \
"    gl_FragColor = vec4(position.x, position.y, v_cursor.x, 1.0);" \
"}";

GLuint CreateShader(const char** source, GLenum type)
{
    GLuint shader = glCreateShader(type);
    GLint length = strlen(*source);
    glShaderSource(shader, 1, source, &length);
    glCompileShader(shader);
    GLint params = 0;
    glGetShaderiv(shader, GL_COMPILE_STATUS, &params);
    if (params == 0)
    {
        GLchar buffer[255] = "";
        GLint length = 255;
        glGetShaderInfoLog(shader, length, &length, buffer);
        printf("[WARN]: CreateShader: %s\n", buffer);
        return 0;
    }
    return shader;
}

GLuint CreateProgram(GLuint vertex, GLuint fragment)
{
    GLuint program = glCreateProgram();
    glAttachShader(program, vertex);
    glAttachShader(program, fragment);
    glLinkProgram(program);
    GLint params = 0;
    glGetProgramiv(program, GL_LINK_STATUS, &params);
    if (params == 0)
    {
        GLchar buffer[255] = "";
        GLint length = 255;
        glGetProgramInfoLog(program, length, &length, buffer);
        printf("[WARN]: CreateProgram: %s\n", buffer);
        return 0;
    }
    return program;
}

GLfloat cursor_data[4] = { 0.0, 0.0, 0.0, 0.0 };
EM_BOOL mouse_event(int eventType, const EmscriptenMouseEvent* mouseEvent, void* userData)
{
    cursor_data[0] = mouseEvent->clientX;
    cursor_data[1] = mouseEvent->clientY;
    printf("[INFO]: Mouse: %f, %f, %f, %f\n", cursor_data[0], cursor_data[1], cursor_data[2], cursor_data[3]);
    return EM_TRUE;
}

int main()
{
    printf("\033[38;5;1m[INFO]:\033[0m %s\n", "TEST");
    EMSCRIPTEN_RESULT result = EMSCRIPTEN_RESULT_SUCCESS;

    EmscriptenWebGLContextAttributes attributes; //= EmscriptenWebGLContextAttributes();
    emscripten_webgl_init_context_attributes(&attributes);
    attributes.alpha = true;
    attributes.depth = true;
    attributes.stencil = true;
    attributes.antialias = true;
    attributes.premultipliedAlpha = true;
    attributes.preserveDrawingBuffer = true;
    attributes.powerPreference = EM_WEBGL_POWER_PREFERENCE_DEFAULT;
    attributes.failIfMajorPerformanceCaveat = false;
    attributes.enableExtensionsByDefault = true;
    attributes.explicitSwapControl = false;
    attributes.renderViaOffscreenBackBuffer = true;
    attributes.proxyContextToMainThread = EMSCRIPTEN_WEBGL_CONTEXT_PROXY_FALLBACK;

    const char* canvas = "canvas";
    EMSCRIPTEN_WEBGL_CONTEXT_HANDLE ctx = emscripten_webgl_create_context(canvas, &attributes);
    printf("[INFO]: Context Handle: %p\n", &ctx);

    result = emscripten_webgl_make_context_current(ctx);
    CHECK(result, "Make Context Current");

    ctx = emscripten_webgl_get_current_context();
    printf("[INFO]: Context Handle: %p\n", &ctx);

    int w = 0;
    int h = 0;

    result = emscripten_webgl_get_drawing_buffer_size(ctx, &w, &h);
    CHECK(result, "Get Canvas Size");
    printf("[INFO]: Canvas Size: width: %d, height: %d\n", w, h);

    w = 1280;
    h = 720;

    //result = emscripten_webgl_set_drawing_buffer_size(ctx, &w, &h);
    result = emscripten_set_canvas_element_size(canvas, w, h);
    CHECK(result, "Set Canvas Size");
    printf("[INFO]: Canvas Size: width: %d, height: %d\n", w, h);

    result = emscripten_webgl_make_context_current(ctx);
    CHECK(result, "Make Context Current");

    result = emscripten_set_mousemove_callback(canvas, 0, true, mouse_event);
    CHECK(result, "Set MouseMove Callback");

    GLuint vertex_shader = CreateShader(&vertex_source, GL_VERTEX_SHADER);
    GLuint fragment_shader = CreateShader(&fragment_source, GL_FRAGMENT_SHADER);
    GLuint shader_program = CreateProgram(vertex_shader, fragment_shader);

    GLuint vertex_attribute = glGetAttribLocation(shader_program, "vertex");
    GLuint vertex_buffer = 0;
    glGenBuffers(1, &vertex_buffer);
    GLfloat vertex_data[] = { -1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, -1.0 };
    GLuint cursor_uniform = glGetUniformLocation(shader_program, "cursor");
    cursor_data[2] = (GLfloat)w;
    cursor_data[3] = (GLfloat)h;

    //BEGIN LOOP//

    while (1)
    {
        glBindFramebuffer(GL_FRAMEBUFFER, 0);
        glViewport(0, 0, w, h);
        glClearColor(0.0, 0.0, 1.0, 1.0);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
 
        glUseProgram(shader_program);

        glEnableVertexAttribArray(vertex_attribute);
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer);
        glBufferData(GL_ARRAY_BUFFER, sizeof(vertex_data), vertex_data, GL_STATIC_DRAW);
        glVertexAttribPointer(vertex_attribute, 2, GL_FLOAT, false, 0, 0);
        glUniform4fv(cursor_uniform, 1, cursor_data);

        glDrawArrays(GL_TRIANGLES, 0, 6);

        emscripten_sleep(0); //yield control to browser scheduler
    }

    //END LOOP//

    result = emscripten_webgl_commit_frame();
    CHECK(result, "Commit Frame");

    return 0;
}
