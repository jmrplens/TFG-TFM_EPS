/**
 * Ejemplo de código JavaScript/TypeScript para demostración en el TFG/TFM.
 * Este archivo puede incluirse con \codigoarchivo{javascript}{recursos/ejemplos/ejemplo.js}
 */

// Clase para gestionar tareas
class TaskManager {
  constructor() {
    this.tasks = [];
    this.nextId = 1;
  }

  /**
   * Añade una nueva tarea
   * @param {string} title - Título de la tarea
   * @param {string} description - Descripción de la tarea
   * @returns {Object} La tarea creada
   */
  addTask(title, description = '') {
    const task = {
      id: this.nextId++,
      title,
      description,
      completed: false,
      createdAt: new Date().toISOString(),
      completedAt: null
    };
    this.tasks.push(task);
    return task;
  }

  /**
   * Marca una tarea como completada
   * @param {number} id - ID de la tarea
   * @returns {boolean} true si se completó correctamente
   */
  completeTask(id) {
    const task = this.tasks.find(t => t.id === id);
    if (task && !task.completed) {
      task.completed = true;
      task.completedAt = new Date().toISOString();
      return true;
    }
    return false;
  }

  /**
   * Obtiene estadísticas de las tareas
   * @returns {Object} Estadísticas
   */
  getStats() {
    const total = this.tasks.length;
    const completed = this.tasks.filter(t => t.completed).length;
    const pending = total - completed;
    
    return {
      total,
      completed,
      pending,
      completionRate: total > 0 ? (completed / total * 100).toFixed(1) : 0
    };
  }

  /**
   * Filtra tareas por estado
   * @param {boolean} completed - Estado de completado
   * @returns {Array} Tareas filtradas
   */
  filterByStatus(completed) {
    return this.tasks.filter(t => t.completed === completed);
  }
}

// Ejemplo de uso con async/await
async function fetchUserData(userId) {
  try {
    const response = await fetch(`/api/users/${userId}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching user:', error.message);
    return null;
  }
}

// Ejemplo de uso
const manager = new TaskManager();

manager.addTask('Redactar introducción', 'Escribir el capítulo de introducción del TFG');
manager.addTask('Revisar bibliografía', 'Actualizar las referencias');
manager.addTask('Crear diagramas', 'Diseñar los diagramas de arquitectura');

manager.completeTask(1);

console.log('Estadísticas:', manager.getStats());
console.log('Tareas pendientes:', manager.filterByStatus(false));

export { TaskManager, fetchUserData };
