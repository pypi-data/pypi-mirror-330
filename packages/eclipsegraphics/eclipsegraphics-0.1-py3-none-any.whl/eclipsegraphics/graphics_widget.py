from __future__ import annotations
from typing import Callable
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt6.QtGui import QColor, QPaintEvent, QPainter
from PyQt6.QtCore import Qt, QPoint, QTimer, QElapsedTimer
import skia
import numpy as np
import math


class Color:
    def __init__(self, r: float, g: float | None = None, b: float | None = None, a: float | None = None):
        if g is None and b is None:  # 1 or 2 value case
            if a is None:  # 1 value case
                self.r = r
                self.g = r
                self.b = r
                self.a = 1.0
            else:  # 2 value case
                self.r = r
                self.g = r
                self.b = r
                self.a = a
        else:  # 3 or 4 value case
            self.r = r
            self.g = g
            self.b = b
            self.a = a if a is not None else 1.0

    def brightness(self, value: float | None = None) -> float:
        # Convert to HSB
        h, s, b = self.to_hsb()

        if value is not None:
            # Set brightness while maintaining hue/saturation
            self.from_hsb(h, s, value)
            return value

        return b

    def to_hsb(self) -> tuple[float, float, float]:
        cmax = max(self.r, self.g, self.b)
        cmin = min(self.r, self.g, self.b)
        delta = cmax - cmin

        # Calculate hue
        if delta == 0:
            h = 0
        elif cmax == self.r:
            h = 60 * (((self.g - self.b) / delta) % 6)
        elif cmax == self.g:
            h = 60 * ((self.b - self.r) / delta + 2)
        else:
            h = 60 * ((self.r - self.g) / delta + 4)

        # Calculate saturation
        s = 0 if cmax == 0 else delta / cmax

        # Calculate brightness
        b = cmax

        return h, s, b

    def from_hsb(self, h: float, s: float, b: float) -> None:
        c = b * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = b - c

        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x

        self.r = r + m
        self.g = g + m
        self.b = b + m

    def lerp(self, other: Color, factor: float) -> None:
        self.r = self.r + (other.r - self.r) * factor
        self.g = self.g + (other.g - self.g) * factor
        self.b = self.b + (other.b - self.b) * factor
        self.a = self.a + (other.a - self.a) * factor

    def copy(self) -> Color:
        return Color(self.r, self.g, self.b, self.a)

    @staticmethod
    def lerp_colors(a: Color, b: Color, factor: float) -> Color:
        r = a.r + (b.r - a.r) * factor
        g = a.g + (b.g - a.g) * factor
        b = a.b + (b.b - a.b) * factor
        a = a.a + (b.a - a.a) * factor
        return Color(r, g, b, a)

    @staticmethod
    def from_qcolor(color: QColor) -> Color:
        return Color(color.redF(), color.greenF(), color.blueF(), color.alphaF())

    @staticmethod
    def to_qcolor(color: Color) -> QColor:
        return QColor(color.r * 255, color.g * 255, color.b * 255, color.a * 255)

    @staticmethod
    def from_ints(r: int, g: int | None = None, b: int | None = None, a: int | None = None) -> Color:
        if g is None and b is None:  # 1 or 2 value case
            if a is None:  # 1 value case
                return Color(r / 255.0)
            else:  # 2 value case
                return Color(r / 255.0, a=a / 255.0)
        else:  # 3 or 4 value case
            return Color(r / 255.0, g / 255.0, b / 255.0, a / 255.0 if a is not None else 1.0)

    @staticmethod
    def to_ints(color: Color) -> tuple[int, int, int, int]:
        return int(color.r * 255), int(color.g * 255), int(color.b * 255), int(color.a * 255)


class GraphicsObject:
    def __init__(self):
        self.graphics_widget: GraphicsWidget | None = None
        self.is_raycast_hit: bool = False  # Handled by the GraphicsWidget

    def awake(self):  # Called once when the object is added to the GraphicsWidget
        pass

    def raycast_reset(self):  # Called each frame to reset any raycasting variables
        pass

    def raycast(self):  # Called each frame to check if the object is being hit by a raycast
        return False

    def raycast_hit(self):  # Called when the object is hit by a raycast
        pass

    def input(self):  # Called each frame to handle input
        pass

    def update(self):  # Called each frame to update the object
        pass

    def render(self):  # Called each frame to either render the object or set callbacks for the render group system to be rendered after all objects render functions have been called
        pass

    def locked(self):  # Called when the object is locked
        pass

    def unlocked(self):  # Called when the object is unlocked
        pass


class GraphicsModule:
    def __init__(self):
        self.graphics_widget: GraphicsWidget | None = None

    def awake(self):  # Called once when the object is added to the GraphicsWidget
        pass

    def input(self):  # Called each frame to handle input
        pass

    def update(self):  # Called each frame to update the object
        pass

    def render(self):  # Called each frame to either render the object or set callbacks for the render group system to be rendered after all objects render functions have been called
        pass

    def locked(self):  # Called when the object is locked
        pass

    def unlocked(self):  # Called when the object is unlocked
        pass


class GraphicsWidget(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        # Window and App
        self.created_window: QMainWindow | None = None
        self.created_app: QApplication | None = None

        # Skia Surface and Canvas
        self.skia_surface: skia.Surface | None = None
        self.skia_canvas: skia.Canvas | None = None
        self.needs_surface_update = True

        # Visual Settings
        self.background_color = Color.from_ints(21, 21, 21)

        # Enable mouse tracking for smooth camera movement
        self.setMouseTracking(True)

        # Enable key tracking
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Time tracking
        self.current_time: float = 0.0
        self.delta_time: float = 0.0
        self.last_update_time: float = 0.0

        # Transformations
        self.render_x = 0
        self.render_y = 0
        self.render_scale = 1.0

        self.target_render_x = 0
        self.target_render_y = 0
        self.target_render_scale = 1.0

        self.target_lerp_factor = 0.4

        self.min_render_scale = 0.1
        self.max_render_scale = 10.0

        # Mouse state
        self.screen_mouse_pos = QPoint()
        self.world_mouse_pos = QPoint()
        self.last_mouse_drag_pos = QPoint()
        self.is_panning = False
        self.left_mouse_down_prev = False
        self.left_mouse_down = False
        self.left_mouse_pressed = False
        self.left_mouse_released = False
        self.right_mouse_down_prev = False
        self.right_mouse_down = False
        self.right_mouse_pressed = False
        self.right_mouse_released = False
        self.middle_mouse_down_prev = False
        self.middle_mouse_down = False
        self.middle_mouse_pressed = False
        self.middle_mouse_released = False

        # Keyboard state
        self.keys_down = set()
        self.keys_pressed = set()
        self.keys_released = set()
        self.modifiers_down = set()
        self.modifiers_pressed = set()
        self.modifiers_released = set()

        # Render Groups
        self.render_groups: dict[float, list[Callable]] = {}

        # Graphics Objects
        self.graphics_objects: list[GraphicsObject] = []
        self.locked_object: GraphicsObject | None = None

        # Graphics Modules
        self.graphics_modules: list[GraphicsModule] = []
        self.locked_module: GraphicsModule | None = None

        # Next Functions
        self.next_callbacks: list[Callable] = []

        # Setup update timer for smooth interpolation and object updates
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.on_timer_update)
        self.update_timer.start(16)  # ~60 FPS

    # World Transformation Functions

    def get_render_pos(self):
        return self.render_x, self.render_y

    def set_render_pos(self, x: float, y: float):
        self.target_render_x = x
        self.target_render_y = y

    def set_render_pos_instant(self, x: float, y: float):
        self.render_x = x
        self.render_y = y
        self.target_render_x = x
        self.target_render_y = y

    def get_render_scale(self):
        return self.render_scale

    def set_render_scale(self, scale: float):
        self.target_render_scale = scale

    def set_render_scale_instant(self, scale: float):
        self.render_scale = scale
        self.target_render_scale = scale

    # Mouse Functions

    def get_mouse_pos(self):
        """Get current mouse position in world coordinates"""
        return self.screen_to_world(self.screen_mouse_pos.x(), self.screen_mouse_pos.y())

    # Render Functions

    def add_render_group(self, group_index: int, callback: Callable):
        """Adds a callback to a list for this group index"""
        if group_index not in self.render_groups:
            self.render_groups[group_index] = []
        self.render_groups[group_index].append(callback)
        return self

    # Graphics Object Functions

    def add_object(self, object: GraphicsObject):
        self.graphics_objects.append(object)
        object.graphics_widget = self
        object.awake()
        return object

    def lock_object(self, object: GraphicsObject | None = None):
        if self.locked_object != None:
            self.locked_object.unlocked()
        self.locked_object = object
        if self.locked_object != None:
            self.locked_object.locked()
        return self

    def unlock_object(self):
        if self.locked_object != None:
            self.locked_object.unlocked()
            self.locked_object = None
        return self

    # Graphics Module Functions

    def add_module(self, module: GraphicsModule):
        self.graphics_modules.append(module)
        module.graphics_widget = self
        module.awake()
        return module

    def remove_module(self, module: GraphicsModule):
        self.graphics_modules.remove(module)
        return self

    def lock_module(self, module: GraphicsModule | None = None):
        if self.locked_module != None:
            self.locked_module.unlocked()
        self.locked_module = module
        if self.locked_module != None:
            self.locked_module.locked()
        return self

    def unlock_module(self):
        if self.locked_module != None:
            self.locked_module.unlocked()
            self.locked_module = None
        return self

    # Next Functions

    def next(self, callback: Callable):
        self.next_callbacks.append(callback)
        return self

    def process_next(self):
        if len(self.next_callbacks) > 0:
            for callback in self.next_callbacks:
                callback()
            self.next_callbacks = []

    # Update Functions

    def on_timer_update(self):
        """Handle timer updates for transform interpolation and object updates"""
        # Update time
        current_time_ms = QApplication.instance().startTimer.elapsed()
        self.current_time = current_time_ms / 1000.0  # Convert to seconds
        self.delta_time = self.current_time - self.last_update_time
        self.last_update_time = self.current_time

        # Update current mouse position
        self.screen_mouse_pos = self.mapFromGlobal(self.cursor().pos())

        # Update world mouse position
        world_x, world_y = self.screen_to_world(
            self.screen_mouse_pos.x(), self.screen_mouse_pos.y())
        self.world_mouse_pos.setX(int(world_x))
        self.world_mouse_pos.setY(int(world_y))

        # Update mouse button states
        self.left_mouse_down_prev = self.left_mouse_down
        self.right_mouse_down_prev = self.right_mouse_down
        self.middle_mouse_down_prev = self.middle_mouse_down
        buttons = QApplication.mouseButtons()
        self.left_mouse_down = bool(buttons & Qt.MouseButton.LeftButton)
        self.right_mouse_down = bool(buttons & Qt.MouseButton.RightButton)
        self.middle_mouse_down = bool(buttons & Qt.MouseButton.MiddleButton)
        self.left_mouse_pressed = self.left_mouse_down and not self.left_mouse_down_prev
        self.left_mouse_released = not self.left_mouse_down and self.left_mouse_down_prev
        self.right_mouse_pressed = self.right_mouse_down and not self.right_mouse_down_prev
        self.right_mouse_released = not self.right_mouse_down and self.right_mouse_down_prev
        self.middle_mouse_pressed = self.middle_mouse_down and not self.middle_mouse_down_prev
        self.middle_mouse_released = not self.middle_mouse_down and self.middle_mouse_down_prev

        # Update modifier states
        current_modifiers = QApplication.keyboardModifiers()

        # Track pressed and released states for modifiers
        for modifier in [Qt.KeyboardModifier.ShiftModifier, Qt.KeyboardModifier.ControlModifier, Qt.KeyboardModifier.AltModifier]:
            is_down = bool(current_modifiers & modifier)
            was_down = modifier in self.modifiers_down

            if is_down and not was_down:
                self.modifiers_pressed.add(modifier)
                self.modifiers_down.add(modifier)
            elif not is_down and was_down:
                self.modifiers_released.add(modifier)
                self.modifiers_down.remove(modifier)

        # First handle transform interpolation
        self.interpolate_transform()

        # Then update all objects and other update specific things
        self.process_update()

        # Clear one-frame states at the END of the frame, after all processing is done
        self.keys_pressed.clear()
        self.keys_released.clear()
        self.modifiers_pressed.clear()
        self.modifiers_released.clear()

    def lerp(self, start: float, end: float, factor: float):
        """Linear interpolation between start and end values"""
        return start + (end - start) * factor

    def interpolate_transform(self):
        """Interpolate between current and target transform values"""
        # Check if we need to update pan
        if abs(self.target_render_x - self.render_x) > 0.01 or abs(self.target_render_y - self.render_y) > 0.01:
            self.render_x = self.lerp(
                self.render_x, self.target_render_x, self.target_lerp_factor)
            self.render_y = self.lerp(
                self.render_y, self.target_render_y, self.target_lerp_factor)

        # Check if we need to update zoom
        if abs(self.target_render_scale - self.render_scale) > 0.0001:
            self.render_scale = self.lerp(
                self.render_scale, self.target_render_scale, self.target_lerp_factor)

        # Always update to ensure continuous frame updates
        self.update()

    def process_update(self):
        # Call all raycast reset functions
        for object in self.graphics_objects:
            object.is_raycast_hit = False
            object.raycast_reset()

        # Process all next callbacks
        self.process_next()

        # Call all raycast in reversed order, stopping at the first hit
        for object in reversed(self.graphics_objects):
            if object.raycast():
                object.is_raycast_hit = True
                object.raycast_hit()
                break

        # Process all next callbacks
        self.process_next()

        # Call all input functions
        if self.locked_object != None:
            self.locked_object.input()
        else:
            for object in self.graphics_objects:
                object.input()
                if self.locked_object != None:  # Stopping if an object becomes locked within the loop
                    break

        # Process all next callbacks
        self.process_next()

        if self.locked_module != None:
            self.locked_module.input()
        else:
            for module in self.graphics_modules:
                module.input()
                if self.locked_module != None:  # Stopping if a module becomes locked within the loop
                    break

        # Process all next callbacks
        self.process_next()

        # Call all update functions
        if self.locked_object != None:
            self.locked_object.update()
        else:
            for object in self.graphics_objects:
                object.update()
                if self.locked_object != None:  # Stopping if an object becomes locked within the loop
                    break

        # Process all next callbacks
        self.process_next()

        if self.locked_module != None:
            self.locked_module.update()
        else:
            for module in self.graphics_modules:
                module.update()
                if self.locked_module != None:  # Stopping if a module becomes locked within the loop
                    break

        # Process all next callbacks
        self.process_next()

    # Render Functions

    def render_objects(self):
        """Render all objects"""
        # Clear stored render groups
        self.render_groups = {}

        # Call all render methods
        for object in self.graphics_objects:
            object.render()

        # Process all next functions
        self.process_next()

        for module in self.graphics_modules:
            module.render()

        # Process all next functions
        self.process_next()

        # Sort render groups and call callbacks in order
        sorted_groups = sorted(self.render_groups.keys())
        for group_index in sorted_groups:
            for callback in self.render_groups[group_index]:
                callback()

        # Process all next functions
        self.process_next()

    def mousePressEvent(self, event):
        """Handle mouse press events"""
        if event.button() == Qt.MouseButton.MiddleButton:
            self.is_panning = True
            self.last_mouse_drag_pos = event.pos()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Handle mouse release events"""
        if event.button() == Qt.MouseButton.MiddleButton:
            self.is_panning = False
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        """Handle mouse move events"""
        # Update current mouse position
        if self.is_panning:
            delta = event.pos() - self.last_mouse_drag_pos
            # Since we're in screen space, we need to divide by scale to get world space delta
            self.target_render_x += delta.x()
            self.target_render_y += delta.y()
            self.last_mouse_drag_pos = event.pos()
        super().mouseMoveEvent(event)

    def wheelEvent(self, event):
        """Handle mouse wheel events for zooming"""
        # Get mouse position in screen space
        mouse_pos = event.position()
        mouse_x = mouse_pos.x()
        mouse_y = mouse_pos.y()

        # Convert to world space before zoom
        old_world_x, old_world_y = self.screen_to_world(mouse_x, mouse_y)

        # Calculate new zoom level
        zoom_factor = 1.2 if event.angleDelta().y() > 0 else 1/1.2
        new_scale = self.target_render_scale * zoom_factor

        # Clamp zoom level
        if self.min_render_scale <= new_scale <= self.max_render_scale:
            # Set the new scale
            self.target_render_scale = new_scale

            # Calculate new world position after zoom to keep mouse point stable
            new_screen_x = old_world_x * new_scale + self.target_render_x + self.width()/2
            new_screen_y = old_world_y * new_scale + self.target_render_y + self.height()/2

            # Adjust offset to maintain mouse position
            self.target_render_x += mouse_x - new_screen_x
            self.target_render_y += mouse_y - new_screen_y

        event.accept()

    def keyPressEvent(self, event):
        """Handle key press events"""
        key = event.key()

        # Only handle regular keys here, modifiers are handled in timer update
        if key not in self.keys_down and key not in (Qt.Key.Key_Shift, Qt.Key.Key_Control, Qt.Key.Key_Alt, Qt.Key.Key_Meta):
            self.keys_pressed.add(key)
            self.keys_down.add(key)

        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        """Handle key release events"""
        key = event.key()

        # Only handle regular keys here, modifiers are handled in timer update
        if key in self.keys_down:
            self.keys_released.add(key)
            self.keys_down.remove(key)

        super().keyReleaseEvent(event)

    def get_key(self, key: int) -> bool:
        """Check if a key is currently held down"""
        if key in (Qt.Key.Key_Shift, Qt.Key.Key_Control, Qt.Key.Key_Alt, Qt.Key.Key_Meta):
            modifier_map = {
                Qt.Key.Key_Shift: Qt.KeyboardModifier.ShiftModifier,
                Qt.Key.Key_Control: Qt.KeyboardModifier.ControlModifier,
                Qt.Key.Key_Alt: Qt.KeyboardModifier.AltModifier,
                Qt.Key.Key_Meta: Qt.KeyboardModifier.MetaModifier
            }
            return modifier_map[key] in self.modifiers_down
        return key in self.keys_down

    def get_key_down(self, key: int) -> bool:
        """Check if a key was just pressed this frame"""
        if key in (Qt.Key.Key_Shift, Qt.Key.Key_Control, Qt.Key.Key_Alt, Qt.Key.Key_Meta):
            modifier_map = {
                Qt.Key.Key_Shift: Qt.KeyboardModifier.ShiftModifier,
                Qt.Key.Key_Control: Qt.KeyboardModifier.ControlModifier,
                Qt.Key.Key_Alt: Qt.KeyboardModifier.AltModifier,
                Qt.Key.Key_Meta: Qt.KeyboardModifier.MetaModifier
            }
            return modifier_map[key] in self.modifiers_pressed
        return key in self.keys_pressed

    def get_key_up(self, key: int) -> bool:
        """Check if a key was just released this frame"""
        if key in (Qt.Key.Key_Shift, Qt.Key.Key_Control, Qt.Key.Key_Alt, Qt.Key.Key_Meta):
            modifier_map = {
                Qt.Key.Key_Shift: Qt.KeyboardModifier.ShiftModifier,
                Qt.Key.Key_Control: Qt.KeyboardModifier.ControlModifier,
                Qt.Key.Key_Alt: Qt.KeyboardModifier.AltModifier,
                Qt.Key.Key_Meta: Qt.KeyboardModifier.MetaModifier
            }
            return modifier_map[key] in self.modifiers_released
        return key in self.keys_released

    # Conversion Functions

    def screen_to_world(self, screen_x, screen_y):
        """Convert screen coordinates to world coordinates"""
        # First subtract window center
        width = self.width()
        height = self.height()
        screen_x -= width/2
        screen_y -= height/2

        # Then apply inverse camera transform
        world_x = (screen_x - self.render_x) / self.render_scale
        world_y = (screen_y - self.render_y) / self.render_scale
        return world_x, world_y

    def world_to_screen(self, world_x, world_y):
        """Convert world coordinates to screen coordinates"""
        # First apply camera transform
        screen_x = world_x * self.render_scale + self.render_x
        screen_y = world_y * self.render_scale + self.render_y

        # Then add window center
        width = self.width()
        height = self.height()
        screen_x += width/2
        screen_y += height/2
        return screen_x, screen_y

    # Creation Functions

    def cleanup(self):
        """Clean up resources"""
        # Stop the update timer
        if self.update_timer:
            self.update_timer.stop()

        # Clear object references
        self.graphics_objects.clear()
        self.graphics_modules.clear()
        self.render_groups.clear()
        self.next_callbacks.clear()

        self.locked_object = None
        self.locked_module = None

    @staticmethod
    def create_window(width: int = 1200, height: int = 800, title: str = "Graphics Widget") -> GraphicsWidget:
        app = QApplication([])

        app.startTimer = QElapsedTimer()
        app.startTimer.start()

        graphics_widget = GraphicsWidget()
        # Use our custom window class
        window = GraphicsMainWindow(graphics_widget)
        window.setWindowTitle(title)
        # Get the screen geometry and calculate center position
        screen = app.primaryScreen().geometry()
        x = (screen.width() - width) // 2
        y = (screen.height() - height) // 2
        window.setGeometry(x, y, width, height)

        window.setCentralWidget(graphics_widget)
        graphics_widget.created_window = window
        graphics_widget.created_app = app

        return graphics_widget

    def run(self):
        if self.created_window != None and self.created_app != None:
            self.created_window.show()
            try:
                self.created_app.exec()
            finally:
                self.cleanup()

    # Draw Functions
    def draw_line(self, ax: float, ay: float, bx: float, by: float, thickness: float = 2,
                  start_color: Color = Color.from_ints(255, 255, 255), end_color: Color | None = None) -> None:
        """Draw a line from point A to point B with optional gradient color"""
        if not self.skia_canvas:
            return

        paint = skia.Paint(
            AntiAlias=True,
            StrokeWidth=thickness,
            Style=skia.Paint.kStroke_Style
        )

        if end_color is None:
            # Single color line
            paint.setColor(skia.Color4f(
                start_color.b,
                start_color.g,
                start_color.r,
                start_color.a
            ))
            self.skia_canvas.drawLine(ax, ay, bx, by, paint)
        else:
            # Gradient line
            points = [(ax, ay), (bx, by)]
            colors = [
                skia.Color4f(start_color.b, start_color.g,
                             start_color.r, start_color.a),
                skia.Color4f(end_color.b, end_color.g,
                             end_color.r, end_color.a)
            ]
            shader = skia.GradientShader.MakeLinear(
                points=points,
                colors=colors
            )
            paint.setShader(shader)
            self.skia_canvas.drawLine(ax, ay, bx, by, paint)

    def draw_rect(self, x: float, y: float, width: float, height: float, color: Color) -> None:
        """Draw a filled rectangle"""
        if not self.skia_canvas:
            return

        paint = skia.Paint(
            AntiAlias=True,
            Color=skia.Color4f(
                color.b,
                color.g,
                color.r,
                color.a
            )
        )
        self.skia_canvas.drawRect(
            skia.Rect(x, y, x + width, y + height), paint)

    def draw_rect_outline(self, x: float, y: float, width: float, height: float,
                          thickness: float, color: Color) -> None:
        """Draw a rectangle outline"""
        if not self.skia_canvas:
            return

        paint = skia.Paint(
            AntiAlias=True,
            StrokeWidth=thickness,
            Style=skia.Paint.kStroke_Style,
            Color=skia.Color4f(
                color.b,
                color.g,
                color.r,
                color.a
            )
        )
        self.skia_canvas.drawRect(
            skia.Rect(x, y, x + width, y + height), paint)

    def draw_circle(self, x: float, y: float, size: float, color: Color) -> None:
        """Draw a filled circle where size is the diameter"""
        if not self.skia_canvas:
            return

        radius = size / 2
        paint = skia.Paint(
            AntiAlias=True,
            Color=skia.Color4f(
                color.b,
                color.g,
                color.r,
                color.a
            )
        )
        self.skia_canvas.drawCircle(x, y, radius, paint)

    def draw_circle_outline(self, x: float, y: float, size: float, thickness: float,
                            color: Color) -> None:
        """Draw a circle outline where size is the diameter"""
        if not self.skia_canvas:
            return

        radius = size / 2
        paint = skia.Paint(
            AntiAlias=True,
            StrokeWidth=thickness,
            Style=skia.Paint.kStroke_Style,
            Color=skia.Color4f(
                color.b,
                color.g,
                color.r,
                color.a
            )
        )
        self.skia_canvas.drawCircle(x + radius, y + radius, radius, paint)

    def draw_text(self, text: str, x: float, y: float, font_size: float, color: Color) -> None:
        """Draw text at the specified position"""
        if not self.skia_canvas:
            return

        paint = skia.Paint(
            AntiAlias=True,
            Color=skia.Color4f(
                color.b,
                color.g,
                color.r,
                color.a
            )
        )
        font = skia.Font(skia.Typeface('Arial'), font_size)
        # Add font_size to y to align with baseline
        self.skia_canvas.drawString(text, x, y + font_size, font, paint)

    def draw_text_wrapped(self, text: str, x: float, y: float, width: float, height: float,
                          font_size: float, color: Color) -> None:
        """Draw text wrapped within a specified rectangle"""
        if not self.skia_canvas:
            return

        paint = skia.Paint(
            AntiAlias=True,
            Color=skia.Color4f(
                color.b,
                color.g,
                color.r,
                color.a
            )
        )
        font = skia.Font(skia.Typeface('Arial'), font_size)
        line_height = font.getSpacing()

        # Split text into words
        words = text.split()
        if not words:
            return

        # Process text line by line
        current_line = []
        current_x = 0
        current_y = y + font_size  # Start position (including baseline offset)
        space_width = font.measureText(" ")

        for word in words:
            word_width = font.measureText(word)

            # If adding this word would exceed width
            if current_line and current_x + word_width > width:
                # Draw current line
                line_text = " ".join(current_line)
                self.skia_canvas.drawString(
                    line_text, x, current_y, font, paint)

                # Move to next line
                current_y += line_height
                if current_y - y > height:  # Stop if we exceed height
                    break

                # Start new line with current word
                current_line = [word]
                current_x = word_width + space_width
            else:
                # Add word to current line
                current_line.append(word)
                current_x += word_width + space_width

        # Draw remaining text if any
        if current_line and current_y - y <= height:
            line_text = " ".join(current_line)
            self.skia_canvas.drawString(line_text, x, current_y, font, paint)

    def draw_polygon(self, points: list[tuple[float, float]], x: float = 0, y: float = 0, color: Color = Color.from_ints(255, 255, 255)) -> None:
        """Draw a filled polygon with the given points, optionally offset by x,y"""
        if not self.skia_canvas or len(points) < 3:
            return

        # Create a path for the polygon
        path = skia.Path()
        
        # Move to the first point
        first_x, first_y = points[0]
        path.moveTo(first_x + x, first_y + y)
        
        # Add lines to all other points
        for px, py in points[1:]:
            path.lineTo(px + x, py + y)
        
        # Close the path back to the first point
        path.close()
        
        # Create paint with fill
        paint = skia.Paint(
            AntiAlias=True,
            Color=skia.Color4f(
                color.b,
                color.g,
                color.r,
                color.a
            )
        )
        
        # Draw the filled path
        self.skia_canvas.drawPath(path, paint)

    def resizeEvent(self, event):
        """Handle widget resize events by recreating the Skia surface"""
        super().resizeEvent(event)
        self.needs_surface_update = True

    def paintEvent(self, event: QPaintEvent):
        """Handle paint events by drawing with Skia"""
        # Create or recreate surface if needed
        if self.needs_surface_update or self.skia_surface is None:
            width = self.width()
            height = self.height()
            if width > 0 and height > 0:  # Ensure valid dimensions
                # Create Skia surface with the same size as the widget
                info = skia.ImageInfo.MakeN32Premul(width, height)
                self.skia_surface = skia.Surface.MakeRaster(info)
                self.skia_canvas = self.skia_surface.getCanvas()
            self.needs_surface_update = False

        if self.skia_surface and self.skia_canvas:
            # Clear the canvas with background color
            self.skia_canvas.clear(skia.Color4f(
                self.background_color.b,
                self.background_color.g,
                self.background_color.r,
                self.background_color.a
            ))

            # Apply world space transformation
            self.skia_canvas.save()

            # First translate to center of window
            width = self.width()
            height = self.height()
            self.skia_canvas.translate(width/2, height/2)

            # Then apply camera transform
            self.skia_canvas.translate(self.render_x, self.render_y)
            self.skia_canvas.scale(self.render_scale, self.render_scale)

            # Render all objects
            self.render_objects()

            # Restore transformation
            self.skia_canvas.restore()

            # Draw the Skia surface to the Qt widget
            image = self.skia_surface.makeImageSnapshot()
            if image:
                # Convert Skia image to QImage format
                byte_data = image.tobytes()
                if byte_data:
                    from PyQt6.QtGui import QImage
                    qt_image = QImage(
                        byte_data,
                        image.width(),
                        image.height(),
                        image.width() * 4,  # Bytes per line (4 bytes per pixel for RGBA)
                        QImage.Format.Format_RGBA8888_Premultiplied
                    )
                    painter = QPainter(self)
                    painter.drawImage(0, 0, qt_image)
                    painter.end()


class GraphicsMainWindow(QMainWindow):
    def __init__(self, graphics_widget: GraphicsWidget):
        super().__init__()
        self.graphics_widget = graphics_widget

    def closeEvent(self, event):
        self.graphics_widget.cleanup()
        super().closeEvent(event)


class DrawFunctionTestObject(GraphicsObject):
    def __init__(self):
        super().__init__()
        self.name = "Draw Function Test Object"

    def render(self):
        # Draw rectangles
        self.graphics_widget.draw_rect(-550, -350,
                                       200, 150, Color.from_ints(255, 100, 100))
        self.graphics_widget.draw_rect_outline(
            -550, -150, 200, 150, 4, Color.from_ints(100, 255, 100))

        # Draw circles
        self.graphics_widget.draw_circle(-300, -
                                         350, 150, Color.from_ints(100, 100, 255))
        self.graphics_widget.draw_circle_outline(
            -300, -150, 150, 4, Color.from_ints(255, 255, 100))

        # Draw lines
        start_color = Color.from_ints(255, 100, 255)
        end_color = Color.from_ints(100, 255, 255)
        self.graphics_widget.draw_line(
            0, -350, 200, -200, 4, start_color, end_color)
        self.graphics_widget.draw_line(
            0, -150, 200, 0, 4, Color.from_ints(255, 255, 255))

        # Draw text
        self.graphics_widget.draw_text(
            "Regular Text", 0, 50, 32, Color.from_ints(255, 255, 255))

        # Draw text wrap area outline
        self.graphics_widget.draw_rect_outline(
            0, 100, 400, 200, 2, Color.from_ints(255, 0, 0))

        self.graphics_widget.draw_text_wrapped(
            "This is wrapped text that will automatically fit within the specified width. It can span multiple lines and demonstrates text wrapping functionality.",
            0, 100, 400, 200, 24, Color.from_ints(200, 200, 200)
        )


class InteractiveObject(GraphicsObject):
    def __init__(self):
        super().__init__()


class InteractiveRect(InteractiveObject):
    def __init__(self, x: float = 0, y: float = 0, width: float = 100, height: float = 100):
        super().__init__()
        # Transform
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # RaycastState
        self.is_hovered = False
        self.relative_mouse_x = 0
        self.relative_mouse_y = 0
        self.normalized_mouse_x = 0
        self.normalized_mouse_y = 0

        # Render
        self.color = Color.from_ints(255, 255, 255)

    def raycast_reset(self):
        self.is_hovered = False
        self.relative_mouse_x = 0
        self.relative_mouse_y = 0
        self.normalized_mouse_x = 0
        self.normalized_mouse_y = 0

    def raycast(self):
        # Get mouse position in world space
        mouse_x, mouse_y = self.graphics_widget.get_mouse_pos()

        # Calculate relative mouse position and normalized mouse position
        self.relative_mouse_x = mouse_x - self.x
        self.relative_mouse_y = mouse_y - self.y
        self.normalized_mouse_x = self.relative_mouse_x / self.width
        self.normalized_mouse_y = self.relative_mouse_y / self.height

        # Check if mouse is within rect
        hit = False
        if mouse_x >= self.x and mouse_x <= self.x + self.width and mouse_y >= self.y and mouse_y <= self.y + self.height:
            self.is_hovered = True
            hit = True

        return hit

    def render(self):
        self.graphics_widget.draw_rect(
            self.x, self.y, self.width, self.height, self.color)


class InteractiveCircle(InteractiveObject):
    def __init__(self, x: float = 0, y: float = 0, radius: float = 50):
        super().__init__()
        # Transform
        self.x = x
        self.y = y
        self.radius = radius

        # RaycastState
        self.is_hovered = False
        # Distance from center (0 to radius)
        self.distance_from_center = 0
        # Normalized distance (0 to 1)
        self.normalized_distance = 0
        # Angle in radians (0 to 2π)
        self.angle = 0
        # Normalized angle (0 to 1)
        self.normalized_angle = 0

        # Render
        self.color = Color.from_ints(255, 255, 255)

    def raycast_reset(self):
        self.is_hovered = False
        self.distance_from_center = 0
        self.normalized_distance = 0
        self.angle = 0
        self.normalized_angle = 0

    def raycast(self):
        # Get mouse position in world space
        mouse_x, mouse_y = self.graphics_widget.get_mouse_pos()

        # Calculate relative position from center
        dx = mouse_x - self.x
        dy = mouse_y - self.y

        # Calculate polar coordinates
        self.distance_from_center = (dx * dx + dy * dy) ** 0.5
        self.normalized_distance = min(1.0, self.distance_from_center / self.radius)
        self.angle = math.atan2(dy, dx)
        if self.angle < 0:
            self.angle += 2 * math.pi
        self.normalized_angle = self.angle / (2 * math.pi)

        # Check if mouse is within circle
        hit = self.distance_from_center <= self.radius
        self.is_hovered = hit
        return hit

    def render(self):
        self.graphics_widget.draw_circle(
            self.x, self.y, self.radius * 2, self.color)


class InteractiveLine(InteractiveObject):
    def __init__(self, ax: float = 0, ay: float = 0, bx: float = 100, by: float = 100):
        super().__init__()
        # Transform
        self.ax = ax
        self.ay = ay
        self.bx = bx
        self.by = by

        # RaycastState
        self.is_hovered = False
        # Progress along line (0 to 1)
        self.progress = 0
        # Distance from line
        self.distance = 0
        # Normalized distance based on line length
        self.normalized_distance = 0
        # Side of line (-1 for left, 1 for right)
        self.side = 0

        # Render
        self.color = Color.from_ints(255, 255, 255)
        self.thickness = 2

    def raycast_reset(self):
        self.is_hovered = False
        self.progress = 0
        self.distance = 0
        self.normalized_distance = 0
        self.side = 0

    def raycast(self):
        # Get mouse position in world space
        mouse_x, mouse_y = self.graphics_widget.get_mouse_pos()

        # Calculate line vector
        dx = self.bx - self.ax
        dy = self.by - self.ay
        line_length = (dx * dx + dy * dy) ** 0.5

        if line_length == 0:
            return False

        # Calculate normalized line vector
        nx = dx / line_length
        ny = dy / line_length

        # Calculate vector to mouse
        mx = mouse_x - self.ax
        my = mouse_y - self.ay

        # Calculate progress along line using dot product
        self.progress = max(0, min(1, (mx * nx + my * ny) / line_length))

        # Calculate closest point on line
        closest_x = self.ax + dx * self.progress
        closest_y = self.ay + dy * self.progress

        # Calculate distance from line
        dx_to_mouse = mouse_x - closest_x
        dy_to_mouse = mouse_y - closest_y
        self.distance = (dx_to_mouse * dx_to_mouse + dy_to_mouse * dy_to_mouse) ** 0.5
        self.normalized_distance = self.distance / line_length

        # Calculate which side of the line the mouse is on
        self.side = 1 if dx_to_mouse * ny - dy_to_mouse * nx > 0 else -1

        # Check if mouse is close enough to line
        hit = self.distance <= self.thickness
        self.is_hovered = hit
        return hit

    def render(self):
        self.graphics_widget.draw_line(
            self.ax, self.ay, self.bx, self.by, self.thickness, self.color)


class InteractivePolygon(InteractiveObject):
    def __init__(self, points: list[tuple[float, float]] = None):
        super().__init__()
        # Transform
        self.points = points or [(0, 0), (100, 0), (100, 100), (0, 100)]
        self.x = 0
        self.y = 0

        # RaycastState
        self.is_hovered = False
        # Barycentric coordinates (weights for each vertex that sum to 1)
        self.barycentric = []
        # Index of closest vertex
        self.closest_vertex = 0
        # Index of closest edge
        self.closest_edge = 0
        # Distance to closest edge
        self.edge_distance = 0
        # Progress along closest edge (0 to 1)
        self.edge_progress = 0

        # Render
        self.color = Color.from_ints(255, 255, 255)

    def raycast_reset(self):
        self.is_hovered = False
        self.barycentric = []
        self.closest_vertex = 0
        self.closest_edge = 0
        self.edge_distance = 0
        self.edge_progress = 0

    def raycast(self):
        # Get mouse position in world space
        mouse_x, mouse_y = self.graphics_widget.get_mouse_pos()

        # Initialize variables for closest point calculation
        num_points = len(self.points)
        min_dist = float('inf')
        self.is_hovered = False

        # Calculate barycentric coordinates
        total_area = 0
        self.barycentric = []
        
        # Calculate areas using triangulation from mouse point
        for i in range(num_points):
            x1, y1 = self.points[i]
            x2, y2 = self.points[(i + 1) % num_points]
            # Area of triangle formed by mouse point and edge
            area = abs((x2 - x1) * (mouse_y - y1) - (mouse_x - x1) * (y2 - y1)) / 2
            total_area += area
            self.barycentric.append(area)

        # Normalize barycentric coordinates
        if total_area > 0:
            self.barycentric = [area / total_area for area in self.barycentric]

        # Find closest edge and vertex
        for i in range(num_points):
            x1, y1 = self.points[i]
            x2, y2 = self.points[(i + 1) % num_points]

            # Check distance to vertex
            dist_to_vertex = ((mouse_x - x1) ** 2 + (mouse_y - y1) ** 2) ** 0.5
            if dist_to_vertex < min_dist:
                min_dist = dist_to_vertex
                self.closest_vertex = i

            # Check distance to edge
            edge_dx = x2 - x1
            edge_dy = y2 - y1
            edge_length = (edge_dx * edge_dx + edge_dy * edge_dy) ** 0.5

            if edge_length > 0:
                # Calculate progress along edge
                progress = max(0, min(1, ((mouse_x - x1) * edge_dx + (mouse_y - y1) * edge_dy) / (edge_length * edge_length)))
                
                # Calculate closest point on edge
                closest_x = x1 + edge_dx * progress
                closest_y = y1 + edge_dy * progress
                
                # Calculate distance to edge
                dist_to_edge = ((mouse_x - closest_x) ** 2 + (mouse_y - closest_y) ** 2) ** 0.5
                
                if dist_to_edge < min_dist:
                    min_dist = dist_to_edge
                    self.closest_edge = i
                    self.edge_distance = dist_to_edge
                    self.edge_progress = progress

        # Check if point is inside polygon using ray casting
        inside = False
        j = num_points - 1
        for i in range(num_points):
            if (((self.points[i][1] > mouse_y) != (self.points[j][1] > mouse_y)) and
                (mouse_x < (self.points[j][0] - self.points[i][0]) * (mouse_y - self.points[i][1]) /
                 (self.points[j][1] - self.points[i][1]) + self.points[i][0])):
                inside = not inside
            j = i

        self.is_hovered = inside
        return inside

    def render(self):
        if len(self.points) >= 3:
            self.graphics_widget.draw_polygon(self.points, self.x, self.y, self.color)



